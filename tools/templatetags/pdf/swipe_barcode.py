import base64

from django import template
from django.utils.safestring import mark_safe
from reportlab.graphics.barcode import createBarcodeImageInMemory

register = template.Library()


@register.simple_tag
def barcode(doc_id):
    bcode = createBarcodeImageInMemory('Code128', value=doc_id, width=250, height=60, isoScale=1, humanReadable=True,
                                       fontName="Helvetica", fontSize=6, format="png")

    png_b64_data = base64.b64encode(bcode).decode("utf-8")

    return mark_safe("<img alt=\"{}\" src=\"data:image/png;base64,{}\"/>".format(doc_id, png_b64_data))
