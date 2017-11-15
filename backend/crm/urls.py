"""
CRM URL Configuration
"""

from django.conf.urls import url

from crm import views

urlpatterns = [
    url(r'^customers/(?P<pk>\d+)$', views.CustomerView.as_view()),
]
