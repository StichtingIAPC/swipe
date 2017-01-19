from django.conf.urls import url

from assortment import api_views as views

urlpatterns = [
    url(r'^search/$', views.search, name='seach'),
    url(r'^all/$', views.all_wishes, name='get_assortment'),
    url(r'^tag_type/(?P<pk>[0-9]+)/$', views.by_label_type, name='get_by_tagtype'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.by_label, name='get_by_tag'),
]
