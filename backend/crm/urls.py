"""
CRM URL Configuration
"""

from django.conf.urls import url

from crm import views

urlpatterns = [
    url(r'^customers/(?P<pk>\d+)$', views.CustomerView.as_view()),
    url(r'^customers/name/$', views.CustomerByNameView.as_view()),
    url(r'^customers/$', views.CustomerListView.as_view()),
    url(r'^persons/(?P<pk>\d+)$', views.PersonView.as_view()),
    url(r'^persons/$', views.PersonCreateView.as_view()),
    url(r'^organisations/(?P<pk>\d+)$', views.OrganisationView.as_view()),
    url(r'^organisations/$', views.OrganisationCreateView.as_view()),
    url(r'^contactorganisations/(?P<pk>\d+)$', views.ContactOrganisationView.as_view()),
    url(r'^contactorganisations/$', views.ContactOrganisationCreateView.as_view()),
]
