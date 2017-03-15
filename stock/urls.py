from django.conf.urls import url

from stock import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.StockView.as_view()),
]