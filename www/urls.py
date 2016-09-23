"""
WWW URL Configuration
"""

from django.conf.urls import url, include
from www.views import home

urlpatterns = [
    # Home page
    url(r'^$', home, name='home'),

    # Include Supplier URLs
    url(r'^supplier/', include('supplier.urls')),

    # Include CRM URLs
    url(r'^crm/', include('crm.urls')),

    # Include Register URLs
    url(r'^register/', include("register.urls")),

    # Include Money URLs
    url(r'^money/', include("money.urls")),

    # Include API URLs
    url(r'^api/', include('api.urls')),

    url(r'^barcode/', include('barcode.urls')),

]
