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
from django.conf.urls import url, include
from django.contrib import admin

import register
from register.views import *

urlpatterns = [
    # Standard page
    url(r'^$', register.views.index, name="register_index"),
    # Django internal documentation
    url(r'^list/', RegisterList.as_view(template_name="register_list.html")),
    url(r'^open/', OpenFormView.as_view(template_name="open_count.html")),
    url(r'^close/', CloseFormView.as_view(template_name="close_count.html")),
    url(r'^list_register/', RegisterList.as_view(template_name="register_list.html")),
    url(r'^list_denomination', DenominationList.as_view(template_name="denomination_list.html")),
    url(r'^add_denomination', DenominationCreate.as_view(template_name="denomination_form.html")),
    url(r'^add_register', RegisterCreate.as_view(template_name="denomination_form.html")),
    url(r'^(?P<pk>[0-9]+)$', DenominationDetail.as_view(), name='denomination_detail'),


]
