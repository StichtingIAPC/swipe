from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from sales.models import Transaction


class SalesPage(ListView):
     model = Transaction