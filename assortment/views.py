from django.shortcuts import render, get_object_or_404

# Create your views here.
from assortment.models import AssortmentLabelType


def search(request):
    pass


def all(request):
    pass


def by_label(request, pk):
    pass


def by_label_type(request, pk):
    label_type = get_object_or_404(AssortmentLabelType, pk=pk)
    relevant_articles = 
