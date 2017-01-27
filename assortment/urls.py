from django.conf.urls import url

from assortment.views import LabelListView, LabelTypeListView, LabelTypeDetailView, UnitTypeListView, UnitTypeDetailView



urlpatterns = [
    url(r'^labels/$', LabelListView.as_view(), name='label_listview'),
    url(r'^labeltypes/$', LabelTypeListView.as_view(), name='labeltype_listview'),
    url(r'^labeltypes/(?P<pk>\d+)/$', LabelTypeDetailView.as_view(), name='labeltype_detailview'),
    url(r'^unittypes/$', UnitTypeListView.as_view(), name='unittype_listview'),
    url(r'^unittypes/(?P<pk>\d+)/$', UnitTypeDetailView.as_view(), name='unittype_detailview'),
]
