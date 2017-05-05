from django.conf import settings
from django.conf.urls import url, include

from tools.views import TableView
from tools.pdf import urls as pdf_urls


app_name = 'tools'
urlpatterns = ()

if settings.DEBUG:
    urlpatterns += (
        url(r'^tabletest/$', TableView.as_view(), name="table_view"),
        url(r'^pdftest/', include(pdf_urls)),
    )
