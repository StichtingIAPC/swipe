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

from money import views

urlpatterns = [
    # Standard page
    url(r'^currency/$', views.CurrencyListView.as_view()),
    url(r'^currency/(?P<pk>[a-zA-Z]{3})/', views.CurrencyView.as_view()),
    url(r'^denomination/(?P<pk>\d+)/', views.DenominationDelete.as_view()),
    url(r'^vat/$', views.VATListView.as_view()),
    url(r'^vat/(?P<pk>\d+)/$', views.VATView.as_view()),
    url(r'^accountinggroup/$', views.AccountingGroupListView.as_view()),
    url(r'^accountinggroup/(?P<pk>\d+)/$', views.AccountingGroupView.as_view())
]
