from django.conf.urls import url

from sales.views import SalesPage
from supplier.views import SupplierList, SupplierDetail, SupplierCreate, SupplierDelete, SupplierEdit

urlpatterns = [
    url(r'^$', SalesPage.as_view(), name='sales'),

]
