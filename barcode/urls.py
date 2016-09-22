"""
CRM URL Configuration
"""

from django.conf.urls import url

from barcode.views import barcode, qr, qr_url

urlpatterns = [
    url(r'^qr/(?P<str>\w{0,5000})/$', qr, name="qr_code"),
    url(r'^qr_url/(?P<str>\w{0,5000})/$', qr_url, name="qr_url_code"),

    url(r'^(?P<str>\w{0,5000})/$', barcode, name="barcode"),

]

