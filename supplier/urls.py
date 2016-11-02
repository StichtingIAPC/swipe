"""
Supplier URL Configuration
"""

from django.conf.urls import url

from supplier.views import SupplierList, SupplierDetail, SupplierCreate, SupplierDelete, SupplierEdit

urlpatterns = [
    url(r'^$', SupplierList.as_view(), name='supplier_list'),
    url(r'^(?P<pk>[0-9]+)/$', SupplierDetail.as_view(), name='supplier_detail'),
    url(r'^add/$', SupplierCreate.as_view(), name='supplier_add'),
    url(r'^(?P<pk>[0-9]+)/delete/$', SupplierDelete.as_view(), name='supplier_delete'),
    url(r'^(?P<pk>[0-9]+)/undelete/$', SupplierDelete.as_view(), name='supplier_undelete'),
    url(r'^(?P<pk>[0-9]+)/edit/$', SupplierEdit.as_view(), name='supplier_edit'),
]
