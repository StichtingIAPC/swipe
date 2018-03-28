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

from register import views

urlpatterns = [
    # Standard page
    url(r'^$', views.RegisterListView.as_view(), name="registerlist_view"),
    url(r'^(?P<pk>\d+)/$', views.RegisterView.as_view(), name="register_view"),
    url(r'^close/$', views.SalesPeriodCloseView.as_view(), name="registeropen_view"),
    url(r'^closed/$', views.RegisterClosedView.as_view(), name="registerclosed_view"),
    url(r'^count/$', views.RegisterCountListView.as_view(), name="registercountlist_view"),
    url(r'^count/(?P<pk>\d+)/$', views.RegisterCountView.as_view(), name="registercount_view"),
    url(r'^lastcounts/$', views.LastCountView.as_view(), name="lastcount_view"),
    url(r'^open/(?P<pk>\d+)/$', views.RegisterOpenView.as_view(), name="registeropen_view"),
    url(r'^opened/$', views.RegisterOpenedView.as_view(), name="registeropened_view"),
    url(r'^paymenttypes/$', views.PaymentTypeListView.as_view(), name="paymenttype_view"),
    url(r'^paymenttypes/(?P<pk>\d+)/$', views.PaymentTypeView.as_view(), name="paymenttype_view"),
    url(r'^paymenttypes/opened/$', views.PaymentTypeOpenListView.as_view(), name="paymenttypeopened_view"),
    url(r'^salesperiods/$', views.SalesPeriodListView.as_view(), name="salesperiodlist_view"),
    url(r'^salesperiods/(?P<pk>\d+)/$', views.SalesPeriodView.as_view(), name="salesperiod_view"),
    url(r'^salesperiods/latest/$', views.SalesPeriodLatestView.as_view(), name="salesperiodlatest_view"),
]
