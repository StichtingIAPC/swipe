from django.http import HttpResponse
from reportlab.graphics.barcode import createBarcodeDrawing

# Create your views here.
from swipe.settings import BASE_URL


def qr(request, string):
    """
        Create QR code for random data
    """
    d = createBarcodeDrawing('QR', value=string)
    d.width *= 3
    d.height *= 3
    d.translate(0, 16)
    d.scale(3, 3)
    binary_stuff = d.asString("gif")
    return HttpResponse(binary_stuff, 'image/gif')


def qr_url(request, string):
    """
        Create QR Code for a url within swipe
    """
    return qr(request, BASE_URL + "/c/" + string)


def barcode(request, string):
    """
        Create BAR code for random data, please keep inputs of reasonable length
    """
    d = createBarcodeDrawing('Code128', value=string, humanReadable=True)
    d.width *= 3
    d.height *= 3
    d.translate(0, 24)
    d.scale(3, 3)
    binary_stuff = d.asString("gif")
    return HttpResponse(binary_stuff, 'image/gif')
