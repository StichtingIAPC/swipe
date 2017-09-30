"""
Supplier URL Configuration
"""

from django.conf.urls import url

from supplier.views import SupplierListView, SupplierView


urlpatterns = [
    url(r'^$', SupplierListView.as_view()),
    url(r'^(?P<pk>\d+)/$', SupplierView.as_view()),
]
