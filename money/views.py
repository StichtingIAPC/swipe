from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from money.models import CurrencyData
# Create your views here.


class CurrencyDataList(ListView):
    model = CurrencyData


def index(request):
    return render(request, 'money/index.html')


class CurrencyDataDetail(DetailView):
    model = CurrencyData


