from decimal import Decimal
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from django.views.generic import View, ListView, CreateView, DetailView

from money.models import Denomination, Price, VAT
from register.forms import CloseForm, OpenForm
from register.models import RegisterMaster, Register, DenominationCount, SalesPeriod, RegisterCount, Transaction


class OpenFormView(View):
    form_class = OpenForm
    initial = {'key': 'value'}
    template_name = 'open_count.html'

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
                                                                 amount=int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])))

                    cnt += denomination.amount * int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])

                reg.open(cnt, request.POST['memo_{}'.format(col.name)], denominations=denomination_counts)

            # <process form cleaned data>
            return HttpResponseRedirect('/register/state/')
        return render(request, self.template_name, {'form': form})


class IsOpenStateView(View):
    template_name = 'is_open_view.html'

    def get(self, request):
        return render(request, self.template_name, {"is_open": RegisterMaster.sales_period_is_open()})


class CloseFormView(View):
    form_class = CloseForm
    initial = {'key': 'value'}
    template_name = 'open_count.html'

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
                    transactions[reg.currency.iso] = Price(Decimal("0.00000"), reg.currency.iso,
                                                           VAT(Decimal("0.00000")))

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
                                                                 amount=int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])))

            SalesPeriod.close(register_counts, denomination_counts, request.POST["MEMO"])
            # <process form cleaned data>
            return HttpResponseRedirect('/register/state/')

        # Stupid user must again...
        return self.get_or_post_from_form(request, form)


class RegisterList(ListView):
    model = Register


class DenominationList(ListView):
    model = Denomination


class DenominationCreate(CreateView):
    model = Denomination
    fields = ['currency', 'amount']
    success_url = reverse_lazy('register_list_denomination')


class RegisterCreate(CreateView):
    model = Register
    fields = ['name', 'currency', 'is_cash_register', 'is_active', 'payment_type']
    success_url = reverse_lazy('list_register')


class DenominationDetail(DetailView):
    model = Denomination


def index(request):
    return render(request, 'index.html')
