from decimal import Decimal

import json
from django.db.models import F
from django.db.models import Prefetch, Count
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponse, JsonResponse
from rest_framework import mixins, generics

from money.models import Denomination, Price, VAT, Currency, Money
from register.models import RegisterMaster, Register, DenominationCount, SalesPeriod, RegisterCount, \
 PaymentType, AlreadyOpenError
from register.serializers import RegisterSerializer, PaymentTypeSerializer, \
    RegisterCountSerializer, SalesPeriodSerializer
from sales.models import Transaction
from tools.templatetags.tools.breadcrumbs import crumb


class RegisterListView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Register.objects.select_related(
        'payment_type'
    ).annotate(
        Count('registercount')
    ).prefetch_related(
                Prefetch(
                    'registercount_set',
                    queryset=RegisterCount.objects.filter(
                        sales_period__endTime__isnull=F('is_opening_count')
                    ).prefetch_related(
                        Prefetch(
                            'denominationcount_set',
                            queryset=DenominationCount.objects.select_related(
                                'denomination'
                            )
                        )
                    )
                )
    ).prefetch_related(
        'currency__denomination_set'
    )  # Heavy prefetch query to optimize loading of objects, and prevent optional O(n) behaviour on the DB
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RegisterOpenedView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    serializer_class = RegisterCountSerializer
    queryset = RegisterCount.objects\
        .filter(sales_period__endTime__isnull=True,
                is_opening_count=True,
                register__is_active=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass
        #obj = RegisterOpenSerializer(request.data)
        #obj.is_valid(raise_exception=True)
        #counts = obj.validated_data['counts']

        #return Response(obj)


class RegisterClosedView(mixins.ListModelMixin,
                        generics.GenericAPIView):
    serializer_class = RegisterCountSerializer

    def get_queryset(self):
        return RegisterMaster.get_last_closed_register_counts()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegisterView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PaymentTypeListView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PaymentTypeView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RegisterCountListView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = RegisterCount.objects.prefetch_related(
        'denominationcount_set__denomination'
    ).prefetch_related(
        'register__currency__denomination_set'
    )
    serializer_class = RegisterCountSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # TODO: insert register count check/validation on creation.
        return self.create(request, *args, **kwargs)


class RegisterCountView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    queryset = RegisterCount.objects.all()
    serializer_class = RegisterCountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RegisterOpenView(mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            register = Register.objects.get(pk=pk)
        except Register.DoesNotExist:
            raise Http404
        json_data=request.data  #type: dict
        print(json_data)
        memo = json_data.get("memo", None)
        if memo is None:
            respo = HttpResponseBadRequest(reason="Memo is missing")
            return respo
        amount = json_data.get("amount", None) # type: str
        if amount is None:
            respo = HttpResponseBadRequest(reason="Amount is missing")
            return respo
        try:
            float(amount)
        except ValueError:
            respo = HttpResponseBadRequest(reason="Amount is malformed")
            return respo
        counted_amount = Decimal(amount)
        denoms = json_data.get("denoms", None)
        if denoms is None:
            respo = HttpResponseBadRequest(reason="Denominationcounts are missing")
            return respo
        if not isinstance(denoms, list):
            respo = HttpResponseBadRequest(reason="Denominationcounts are malformed")
            return respo
        if not register.is_cash_register:
            try:
                count=register.open(counted_amount=counted_amount, memo=memo)
                return HttpResponse(content=json.dumps(RegisterCountSerializer().to_representation(count)),
                                    content_type="application/json")
            except AlreadyOpenError:
                respo = HttpResponseBadRequest(reason="Register is already opened")
                return respo
        print(counted_amount)
        print(type(json_data))
        reg = self.retrieve(request, *args, **kwargs)
        return reg
#
# @crumb(_('Open registers'), 'register_state')
# class OpenFormView(PermissionRequiredMixin, View):
#     permission_required = 'register.open_register'
#     form_class = OpenForm
#     initial = {'key': 'value'}
#     template_name = "register/open_count.html"
#
#     def get(self, request):
#         if RegisterMaster.sales_period_is_open():
#             return HttpResponse("ERROR, Register is already open")
#
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             for col in form.briefs:
#                 if request.POST.get("brief_" + col, False):
#                     reg = Register.objects.get(name=col)
#                     reg.open(Decimal(0), "")
#
#             for col in form.columns:
#                 if not request.POST.get("reg_{}_active".format(col.name), False):
#                     continue
#                 reg = Register.objects.get(name=col.name)
#                 denomination_counts = []
#                 cnt = Decimal(0)
#                 for denomination in Denomination.objects.filter(currency=reg.currency):
#                     denomination_counts.append(DenominationCount(denomination=denomination,
#                                                                  amount=int(request.POST["reg_{}_{}"
#                                                                             .format(col.name, denomination.amount)])))
#
#                     cnt += denomination.amount * int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])
#
#                 reg.open(cnt, request.POST['memo_{}'.format(col.name)], denominations=denomination_counts)
#
#             # <process form cleaned data>
#             return HttpResponseRedirect('/register/state/')
#         return render(request, self.template_name, {'form': form})
#

# @crumb(_('Open check'), 'register_index')
# class IsOpenStateView(LoginRequiredMixin, View):
#     template_name = "register/is_open_view.html"
#
#     def get(self, request):
#         return render(request, self.template_name, {"is_open": RegisterMaster.sales_period_is_open()})
#
#
# @crumb(_('Close registers'), 'register_state')
# class CloseFormView(PermissionRequiredMixin, View):
#     permission_required = 'register.close_register'
#     form_class = CloseForm
#     initial = {'key': 'value'}
#     template_name = "register/close_count.html"
#
#     def get_or_post_from_form(self, request, form):
#         transactions = {}
#         all_transactions = Transaction.objects.filter(salesperiod=RegisterMaster.get_open_sales_period())
#         for trans in all_transactions:
#             if transactions.get(trans.price.currency.iso, False):
#                 transactions[trans.price.currency.iso] += trans.price
#             else:
#                 transactions[trans.price.currency.iso] = trans.price
#         regs = RegisterMaster.get_open_registers()
#         used_currencies = []
#         for reg in regs:
#             if not used_currencies.__contains__(reg.currency):
#                 used_currencies.append(reg.currency)
#                 if not transactions.get(reg.currency.iso, False):
#                     transactions[reg.currency.iso] = Price(Decimal("0.00000"), VAT(Decimal("0.00000")),
#                                                            reg.currency.iso)
#
#         return render(request, self.template_name,
#                       {'form': form, "transactions": transactions, "currencies": used_currencies})
#
#     def get(self, request):
#         if not RegisterMaster.sales_period_is_open():
#             return HttpResponse("ERROR, Register isn't open")
#
#         form = self.form_class(initial=self.initial)
#         return self.get_or_post_from_form(request, form)
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             denomination_counts = []
#             register_counts = []
#             for col in form.briefs:
#                 reg = Register.objects.get(name=col)
#
#                 register_counts.append(RegisterCount(register=reg, sales_period=SalesPeriod.get_opened_sales_period(),
#                                                      amount=Decimal(request.POST["brief_{}".format(col)])))
#
#             for col in form.columns:
#                 reg = Register.objects.get(name=col.name)
#
#                 cnt = Decimal(0)
#
#                 for denomination in Denomination.objects.filter(currency=reg.currency):
#                     cnt += denomination.amount * int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])
#                 rc = RegisterCount(register=reg, sales_period=SalesPeriod.get_opened_sales_period(),
#                                    is_opening_count=False, amount=cnt)
#                 register_counts.append(rc)
#                 for denomination in Denomination.objects.filter(currency=reg.currency):
#                     denomination_counts.append(DenominationCount(register_count=rc, denomination=denomination,
#                                                                  amount=int(request.POST["reg_{}_{}"
#                                                                             .format(col.name, denomination.amount)])))
#
#             SalesPeriod.close(register_counts, denomination_counts, request.POST["MEMO"])
#             # <process form cleaned data>
#             return HttpResponseRedirect('/register/state/')
#
#         # Stupid user must again...
#         return self.get_or_post_from_form(request, form)
#
#
# @crumb(_('Register list'), 'register_index')
# class RegisterList(LoginRequiredMixin, ListView):
#     model = Register
#     template_name = "register/register_list.html"
#
#
# @crumb(_('Detail'), 'register_list')
# class RegisterDetail(LoginRequiredMixin, DetailView):
#     model = Register
#     template_name = "register/register_detail.html"
#
#
# @crumb(_('Edit'), 'register_detail', ['pk'])
# class RegisterEdit(PermissionRequiredMixin, UpdateView):
#     model = Register
#     template_name = 'register/register_form.html'
#     fields = ['name', 'is_active']
#     permission_required = 'register.edit_register'
#
#     def get_success_url(self):
#         return reverse_lazy('register_detail', kwargs=self.kwargs)
#
#
# @crumb(_('Create'), 'register_list')
# class RegisterCreate(PermissionRequiredMixin, CreateView):
#     permission_required = 'register.create_register'
#     template_name = "register/register_form.html"
#
#     model = Register
#     fields = ['name', 'currency', 'is_cash_register', 'is_active', 'payment_type']
#
#     def get_success_url(self):
#         return reverse_lazy('register_detail', kwargs={'pk': self.object.pk})
#
#
# @crumb(_('Register index'))
# def index(request):
#     return render(request, 'register/index.html')
#
#
# @crumb(_('Payment type list'), 'register_index')
# class PaymentTypeList(LoginRequiredMixin, ListView):
#     model = PaymentType
#     template_name = 'register/paymenttype_list.html'
#
#
# @crumb(_('Create'), 'paymenttype_list')
# class PaymentTypeCreate(PermissionRequiredMixin, CreateView):
#     model = PaymentType
#     fields = ['name']
#     permission_required = 'register.create_paymenttype'
#     template_name = 'register/paymenttype_form.html'
#
#     def get_success_url(self):
#         return reverse_lazy('paymenttype_detail', kwargs={'pk': self.object.pk})
#
#
# @crumb(_('Detail'), 'paymenttype_list')
# class PaymentTypeDetail(LoginRequiredMixin, DetailView):
#     model = PaymentType
#     template_name = 'register/paymenttype_detail.html'


class SalesPeriodListView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SalesPeriodView(mixins.RetrieveModelMixin,
                      generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SalesPeriodLatestView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                      generics.GenericAPIView):
    serializer_class = SalesPeriodSerializer

    def get_queryset(self):
        if SalesPeriod.objects.exists():
            return [SalesPeriod.objects.latest('beginTime')]
        else:
            return SalesPeriod.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
