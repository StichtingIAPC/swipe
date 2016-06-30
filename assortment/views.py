import json

from django.shortcuts import render, get_object_or_404

from article.models import WishableType
from assortment.models import AssortmentLabelType


def search(request):
    relevant_wishables = WishableType.objects.all().prefetch_related('labels')
    relevant_labeltypes = AssortmentLabelType.objects\
        .all()\
        .prefetch_related('assortmentlabel_set')


def all(request):
    relevant_wishables = WishableType.objects.all().prefetch_related('labels')
    relevant_labeltypes = AssortmentLabelType.objects\
        .all()\
        .prefetch_related('assortmentlabel_set')
    return json.dumps([*relevant_labeltypes]) + json.dumps()


def by_label(request, pk):
    relevant_wishables = WishableType.objects.filter(labels__id=id)
    return json.dumps([*relevant_wishables])


def by_label_type(request, pk):
    relevant_wishables = WishableType.objects.filter(labels__label_type_id=pk)
    return json.dumps([*relevant_wishables])
