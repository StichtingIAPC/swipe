"""
WWW URL Configuration
"""

from django.conf.urls import url, include

from www.views import home


urlpatterns = [
    # Home page
    url(r'^$', home, name='home'),

    url(r'^auth/', include('authorization.urls')),

    url(r'^article/', include('article.urls')),

    url(r'^assortment/', include('assortment.urls')),

    url(r'^barcode/', include('barcode.urls')),

    url(r'^crm/', include('crm.urls')),

    url(r'^money/', include("money.urls")),

    url(r'^supplier/', include('supplier.urls')),

    url(r'^register/', include('register.urls')),

    url(r'^sales/', include('sales.urls')),

    url(r'^stock/', include('stock.urls')),

    url(r'^tools/', include('tools.urls')),

    url(r'^public/', include('public_info.urls')),

    url(r'^auth/', include('authorization.urls')),

    url(r'^externalise/', include('externalise.urls')),
]
