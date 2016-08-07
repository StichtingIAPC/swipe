from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView
from money.models import CurrencyData
from django.core.urlresolvers import reverse_lazy
# Create your views here.


class CurrencyDataList(ListView):
    model = CurrencyData


def index(request):
    return render(request, 'money/index.html')


class CurrencyDataDetail(DetailView):
    model = CurrencyData


class CurrencyDataCreate(CreateView):
    model = CurrencyData
    fields = ['iso', 'name', 'digits', 'symbol']
    success_url = reverse_lazy('currencydata_list')


