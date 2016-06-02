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

from register.views import index, RegisterList, OpenFormView, CloseFormView, IsOpenStateView, DenominationList,\
                           DenominationCreate, RegisterCreate, DenominationDetail

urlpatterns = [
    # Standard page
    url(r'^$', index, name="register_index"),
    # Django internal documentation
    url(r'^list/', RegisterList.as_view(template_name="register_list.html"), name="register_list"),
    url(r'^open/', OpenFormView.as_view(template_name="open_count.html"), name="register_open"),
    url(r'^close/', CloseFormView.as_view(template_name="close_count.html"), name="register_close"),
    url(r'^state/', IsOpenStateView.as_view(template_name="is_open_view.html"), name="register_state"),

    url(r'^list_register/', RegisterList.as_view(template_name="register_list.html"), name="register_list_register"),
    url(r'^list_denomination', DenominationList.as_view(template_name="denomination_list.html"), name="register_list_denomination"),
    url(r'^add_denomination', DenominationCreate.as_view(template_name="denomination_form.html"), name="register_add_denomination"),
    url(r'^add_register', RegisterCreate.as_view(template_name="denomination_form.html"), name="register_add_register"),
    url(r'^(?P<pk>[0-9]+)$', DenominationDetail.as_view(), name="denomination_detail"),


]
