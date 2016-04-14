from decimal import Decimal
from django.forms import IntegerField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from money.models import Denomination, Money
from register.forms import CloseForm, OpenForm
from register.models import RegisterMaster, Register, DenominationCount, SalesPeriod, RegisterCount


class OpenFormView(View):
    form_class = OpenForm
    initial = {'key': 'value'}
    template_name = 'count.html'

    def get(self, request, *args, **kwargs):
        if RegisterMaster.sales_period_is_open():
            return (HttpResponse("ERROR, Register is already open"))

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            for col in form.briefs:
                print(col)
                if request.POST.get("brief_"+(col), False):
                    reg = Register.objects.get(name=col)
                    reg.open(Decimal(0))

            for col in form.columns:
                print(col.name)
                reg = Register.objects.get(name=col.name)
                denomination_counts = []
                cnt = Decimal(0)
                for denomination in Denomination.objects.filter(currency=reg.currency):
                    denomination_counts.append(DenominationCount(denomination=denomination,amount=int(request.POST["reg_{}_{}".format(col.name,denomination.amount)])))
                    cnt += denomination.amount * int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])

                print(denomination_counts[0].amount)
                reg.open(cnt,denominations=denomination_counts)
            # <process form cleaned data>
                return HttpResponseRedirect('/register/state/')
        return render(request, self.template_name, {'form': form,'rightbar':"HOI"})


class IsOpenStateView(View):
    template_name = 'is_open_view.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{"is_open":RegisterMaster.sales_period_is_open()})


class CloseFormView(View):
    form_class = CloseForm
    initial = {'key': 'value'}
    template_name = 'count.html'

    def get(self, request, *args, **kwargs):

        if not RegisterMaster.sales_period_is_open():
            return (HttpResponse("ERROR, Register isn't open"))
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form,'rightbar':"HOI"})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            denomination_counts = []
            register_counts = []
            for col in form.briefs:
                reg = Register.objects.get(name=col)

                register_counts.append(RegisterCount(register_period=reg.get_current_open_register_period(),amount=Decimal(request.POST["brief_{}".format(col)])))
            for col in form.columns:
                reg = Register.objects.get(name=col.name)

                cnt = Decimal(0)


                for denomination in Denomination.objects.filter(currency=reg.currency):
                    cnt += denomination.amount * int(request.POST["reg_{}_{}".format(col.name, denomination.amount)])
                rc = RegisterCount(register_period=reg.get_current_open_register_period(),is_opening_count=False,amount=cnt)
                register_counts.append(rc)
                for denomination in Denomination.objects.filter(currency=reg.currency):
                    denomination_counts.append(DenominationCount(register_count=rc,denomination=denomination,amount=int(request.POST["reg_{}_{}".format(col.name,denomination.amount)])))

            SalesPeriod.close(register_counts, denomination_counts,"HOI")
            # <process form cleaned data>
            print("CLOSING")
            return HttpResponseRedirect('/register/state/')

        return render(request, self.template_name, {'form': form,'rightbar':"HOI"})