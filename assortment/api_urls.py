from django.conf.urls import url


urlpatterns = [
    url(r'^search/$', None, name='seach'),
    url(r'^all/$', None, name='get_assortment'),
    url(r'^branch/(?P<pk>[0-9]+)/$', None, name='get_by_branch'),
    url(r'^tag_type/(?P<pk>[0-9]+)/$', None, name='get_by_tagtype'),
    url(r'^tag/(?P<pk>[0-9]+)/$', None, name='get_by_tag'),
]
