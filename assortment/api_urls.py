from django.conf.urls import url

from assortment.views import search

urlpatterns = [
    url(r'^search/$', search, name='seach'),
    url(r'^all/$', search, name='get_assortment'),
    url(r'^branch/(?P<pk>[0-9]+)/$', search, name='get_by_branch'),
    url(r'^tag_type/(?P<pk>[0-9]+)/$', search, name='get_by_tagtype'),
    url(r'^tag/(?P<pk>[0-9]+)/$', search, name='get_by_tag'),
]
