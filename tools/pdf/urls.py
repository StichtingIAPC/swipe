from django.conf import settings
from django.conf.urls import url

from tools.pdf.pdf_views import SwipePdfView, HeaderTest, FooterTest, ReceiptPdfTest, InvoicePdfTest, OrderPdfTest, \
    SupplierOrderPdfTest

urlpatterns = ()

if settings.DEBUG:
    urlpatterns += (
        url(r'^swipe/$', SwipePdfView.as_view(), name="swipe_pdf_test"),
        url(r'^header/$', HeaderTest.as_view(), name="header_pdf_test"),
        url(r'^footer/$', FooterTest.as_view(), name="footer_pdf_test"),
        url(r'^receipt/$', ReceiptPdfTest.as_view(), name="receipt_pdf_test"),
        url(r'^invoice/$', InvoicePdfTest.as_view(), name="invoice_pdf_test"),
        url(r'^order/$', OrderPdfTest.as_view(), name="order_pdf_test"),
        url(r'^supplierorder/$', SupplierOrderPdfTest.as_view(), name="supplierorder_pdf_test"),
    )
