import html

from django.http import HttpResponse
from django.shortcuts import render
from reportlab.graphics.barcode import createBarcodeDrawing

# Create your views here.
from swipe.settings import BASE_URL


def qr(request, str):
    """
        Create QR code for random data
    """
    d = createBarcodeDrawing('QR', value=str)
    d.width *= 3
    d.height *= 3
    d.translate(0,16)
    d.scale(3,3)
    binary_stuff = d.asString("gif")
    return HttpResponse(binary_stuff, 'image/gif')


def qr_url(request, str):
    """
        Create QR Code for a url within swipe
    """
    return qr(request, BASE_URL+"/c/"+str)


def barcode(request, str):
    """
        Create BAR code for random data, please keep inputs of reasonable length
    """
    d = createBarcodeDrawing('Code128', value=str, humanReadable=True)
    d.width *= 3
    d.height *= 3
    d.translate(0,24)
    d.scale(3,3)
    binary_stuff = d.asString("gif")
    return HttpResponse(binary_stuff, 'image/gif')

