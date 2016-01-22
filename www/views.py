from django.http import Http404
from django.shortcuts import render


def home(request):
    raise Http404()
