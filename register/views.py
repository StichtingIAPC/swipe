from decimal import Decimal

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Prefetch
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView
from rest_framework import mixins, generics

from money.models import Denomination, Price, VAT
from register.forms import CloseForm, OpenForm
from register.models import RegisterMaster, Register, DenominationCount, SalesPeriod, RegisterCount, \
    RegisterPeriod, PaymentType
from register.serializers import RegisterSerializer, PaymentTypeSerializer, SalesPeriodSerializer
from sales.models import Transaction
from tools.templatetags.tools.breadcrumbs import crumb


class RegisterListView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Register.objects\
        .prefetch_related(Prefetch(
            'registerperiod_set',
            queryset=RegisterPeriod.objects.order_by('endTime')[:5]
            .prefetch_related(Prefetch(
                'registercount_set',
                queryset=RegisterCount.objects.all().prefetch_related(Prefetch(
                    'denominationcount_set',
                    queryset=DenominationCount.objects.all().select_related('denomination')
                ))
            ))
        ))
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RegisterView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    queryset = Register.objects\
        .select_related('payment_type')\
        .prefetch_related(Prefetch(
            'registerperiod_set',
            queryset=RegisterPeriod.objects.order_by('endTime')[:5]
            .prefetch_related(Prefetch(
                'registercount_set',
                queryset=RegisterCount.objects.all().prefetch_related(Prefetch(
                    'denominationcount_set',
                    queryset=DenominationCount.objects.all().select_related('denomination')
                ))
            ))
        ))
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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


class SalesPeriodListView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@crumb(_('Open registers'), 'register_state')
class OpenFormView(PermissionRequiredMixin, View):
    permission_required = 'register.open_register'
    form_class = OpenForm
    initial = {'key': 'value'}
    template_name = "register/open_count.html"

    def get(self, request):
        if RegisterMaster.sales_period_is_open():
            return HttpResponse("ERROR, Register is already open")

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            for col in form.briefs:
                if request.POST.get("brief_" + col, False):
                    reg = Register.objects.get(name=col)
                    reg.open(Decimal(0), "")

            for col in form.columns:
                if not request.POST.get("reg_{}_active".format(col.name), False):
                    continue
                reg = Register.objects.get(name=col.name)
                denomination_counts = []
                cnt = Decimal(0)
                for denomination in Denomination.objects.filter(currency=reg.currency):
                    denomination_counts.append(DenominationCount(denomination=denomination,
                                                                 amount=int(request.POST["reg_{}_{}"
                                                                            .format(col.name, denomination.amount)])))

                    cnt += denomination.amount * int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])

                reg.open(cnt, request.POST['memo_{}'.format(col.name)], denominations=denomination_counts)

            # <process form cleaned data>
            return HttpResponseRedirect('/register/state/')
        return render(request, self.template_name, {'form': form})


@crumb(_('Open check'), 'register_index')
class IsOpenStateView(LoginRequiredMixin, View):
    template_name = "register/is_open_view.html"

    def get(self, request):
        return render(request, self.template_name, {"is_open": RegisterMaster.sales_period_is_open()})


@crumb(_('Close registers'), 'register_state')
class CloseFormView(PermissionRequiredMixin, View):
    permission_required = 'register.close_register'
    form_class = CloseForm
    initial = {'key': 'value'}
    template_name = "register/close_count.html"

    def get_or_post_from_form(self, request, form):
        transactions = {}
        all_transactions = Transaction.objects.filter(salesperiod=RegisterMaster.get_open_sales_period())
        for trans in all_transactions:
            if transactions.get(trans.price.currency.iso, False):
                transactions[trans.price.currency.iso] += trans.price
            else:
                transactions[trans.price.currency.iso] = trans.price
        regs = RegisterMaster.get_open_registers()
        used_currencies = []
        for reg in regs:
            if not used_currencies.__contains__(reg.currency):
                used_currencies.append(reg.currency)
                if not transactions.get(reg.currency.iso, False):
                    transactions[reg.currency.iso] = Price(Decimal("0.00000"), VAT(Decimal("0.00000")),
                                                           reg.currency.iso)

        return render(request, self.template_name,
                      {'form': form, "transactions": transactions, "currencies": used_currencies})

    def get(self, request):
        if not RegisterMaster.sales_period_is_open():
            return HttpResponse("ERROR, Register isn't open")

        form = self.form_class(initial=self.initial)
        return self.get_or_post_from_form(request, form)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            denomination_counts = []
            register_counts = []
            for col in form.briefs:
                reg = Register.objects.get(name=col)

                register_counts.append(RegisterCount(register_period=reg.get_current_open_register_period(),
                                                     amount=Decimal(request.POST["brief_{}".format(col)])))

            for col in form.columns:
                reg = Register.objects.get(name=col.name)

                cnt = Decimal(0)

                for denomination in Denomination.objects.filter(currency=reg.currency):
                    cnt += denomination.amount * int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])
                rc = RegisterCount(register_period=reg.get_current_open_register_period(),
                                   is_opening_count=False, amount=cnt)
                register_counts.append(rc)
                for denomination in Denomination.objects.filter(currency=reg.currency):
                    denomination_counts.append(DenominationCount(register_count=rc, denomination=denomination,
                                                                 amount=int(request.POST["reg_{}_{}"
                                                                            .format(col.name, denomination.amount)])))

            SalesPeriod.close(register_counts, denomination_counts, request.POST["MEMO"])
            # <process form cleaned data>
            return HttpResponseRedirect('/register/state/')

        # Stupid user must again...
        return self.get_or_post_from_form(request, form)


@crumb(_('Register list'), 'register_index')
class RegisterList(LoginRequiredMixin, ListView):
    model = Register
    template_name = "register/register_list.html"


@crumb(_('Detail'), 'register_list')
class RegisterDetail(LoginRequiredMixin, DetailView):
    model = Register
    template_name = "register/register_detail.html"


@crumb(_('Edit'), 'register_detail', ['pk'])
class RegisterEdit(PermissionRequiredMixin, UpdateView):
    model = Register
    template_name = 'register/register_form.html'
    fields = ['name', 'is_active']
    permission_required = 'register.edit_register'

    def get_success_url(self):
        return reverse_lazy('register_detail', kwargs=self.kwargs)


@crumb(_('Register period list'), 'register_index')
class RegisterPeriodList(LoginRequiredMixin, ListView):
    model = RegisterPeriod


@crumb(_('Create'), 'register_list')
class RegisterCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'register.create_register'
    template_name = "register/register_form.html"

    model = Register
    fields = ['name', 'currency', 'is_cash_register', 'is_active', 'payment_type']

    def get_success_url(self):
        return reverse_lazy('register_detail', kwargs={'pk': self.object.pk})


@crumb(_('Register index'))
def index(request):
    return render(request, 'register/index.html')


@crumb(_('Payment type list'), 'register_index')
class PaymentTypeList(LoginRequiredMixin, ListView):
    model = PaymentType
    template_name = 'register/paymenttype_list.html'


@crumb(_('Create'), 'paymenttype_list')
class PaymentTypeCreate(PermissionRequiredMixin, CreateView):
    model = PaymentType
    fields = ['name']
    permission_required = 'register.create_paymenttype'
    template_name = 'register/paymenttype_form.html'

    def get_success_url(self):
        return reverse_lazy('paymenttype_detail', kwargs={'pk': self.object.pk})


@crumb(_('Detail'), 'paymenttype_list')
class PaymentTypeDetail(LoginRequiredMixin, DetailView):
    model = PaymentType
    template_name = 'register/paymenttype_detail.html'
