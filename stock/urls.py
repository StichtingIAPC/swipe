from django.conf.urls import url

from stock import views

urlpatterns = [
    url(r'^$', views.StockListView.as_view()),
    url(r'^c(?P<customer>\d+)/$', views.StockListView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.StockView.as_view()),
    url(r'^c(?P<customer>\d+)/(?P<pk>\d+)/$', views.StockView.as_view()),
]
