from django.conf.urls import url

from assortment import api_views as views

urlpatterns = [
    url(r'^search/$', views.all, name='seach'),
    url(r'^all/$', views.all, name='get_assortment'),
    url(r'^branch/(?P<pk>[0-9]+)/$', views.all, name='get_by_branch'),
    url(r'^tag_type/(?P<pk>[0-9]+)/$', views.all, name='get_by_tagtype'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.all, name='get_by_tag'),
]
