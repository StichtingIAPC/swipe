from django.conf import settings
from django.conf.urls import url

from tools.pdf.pdf_views import SwipePdfView, HeaderTest, FooterTest, ReceiptPdfTest

urlpatterns = ()

if settings.DEBUG:
    urlpatterns += (
        url(r'^swipe/$', SwipePdfView.as_view(), name="swipe_pdf_test"),
        url(r'^header/$', HeaderTest.as_view(), name="header_pdf_test"),
        url(r'^footer/$', FooterTest.as_view(), name="footer_pdf_test"),
        url(r'^receipt/$', ReceiptPdfTest.as_view(), name="receipt_pdf_test"),
    )
