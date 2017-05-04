from django.conf import settings
from django.conf.urls import url

from tools.pdf.base_pdf import PdfView
from tools.pdf.swipe_pdf import SwipePdfView
from tools.views import TableView


app_name = 'tools'
urlpatterns = ()

if settings.DEBUG:
    urlpatterns += (
        url(r'^tabletest/$', TableView.as_view(), name="table_view"),
        url(r'^pdftest/$', SwipePdfView.as_view(), name="pdf_test_view"),
    )
