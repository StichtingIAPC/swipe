from django.shortcuts import render
from django.views.generic import View, ListView
from money.models import CurrencyData
# Create your views here.


class CurrencyDataList(ListView):
    model = CurrencyData

