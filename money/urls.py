"""swipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from money.views import *

urlpatterns = [
    # Standard page
    url(r'^$', index, name="money_index"),
    # Django internal documentation
    url(r'^list/$', CurrencyDataList.as_view(), name="currencydata_list"),
    url(r'^add/$', CurrencyDataCreate.as_view(), name='currencydata_add'),
    url(r'^(?P<pk>[A-Z]+)/$', CurrencyDataDetail.as_view(), name='currencydata_detail'),
    url(r'^(?P<pk>[A-Z]+)/edit/$', CurrencyDataEdit.as_view(), name='currencydata_edit'),

    url(r'^(?P<pk>[A-Z]+)/denominations/$', DenominationList.as_view(), name='denomination_list'),
    url(r'^(?P<pk>[A-Z]+)/denominations/add/$', DenominationCreate.as_view(), name='denomination_add'),
    url(r'^(?P<pk>[A-Z]+)/denominations/(?P<denom>[0-9]+)/$', DenominationDetail.as_view(), name='denomination_detail')
]
