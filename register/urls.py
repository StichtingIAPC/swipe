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

from register.views import index, RegisterList, OpenFormView, CloseFormView, IsOpenStateView, RegisterCreate, \
    RegisterDetail, PaymentTypeList, PaymentTypeCreate, PaymentTypeDetail, RegisterEdit



urlpatterns = [
    # Standard page
    url(r'^$', index, name="register_index"),

    url(r'^state/$', IsOpenStateView.as_view(), name="register_state"),
    url(r'^state/open/$', OpenFormView.as_view(), name="register_open"),
    url(r'^state/close/$', CloseFormView.as_view(), name="register_close"),

    url(r'^list/$', RegisterList.as_view(), name="register_list"),
    url(r'^add/$', RegisterCreate.as_view(), name="register_create"),
    url(r'^(?P<pk>[0-9]+)/$', RegisterDetail.as_view(), name="register_detail"),
    url(r'^(?P<pk>[0-9]+)/edit/', RegisterEdit.as_view(), name="register_edit"),

    url(r'^paymenttypes/$', PaymentTypeList.as_view(), name='paymenttype_list'),
    url(r'^paymenttypes/add/$', PaymentTypeCreate.as_view(), name='paymenttype_create'),
    url(r'^paymenttypes/(?P<pk>[0-9]+)/$', PaymentTypeDetail.as_view(), name='paymenttype_detail'),
]
