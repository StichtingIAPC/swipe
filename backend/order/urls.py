from django.conf.urls import url

from order import views

urlpatterns = [
    # Standard page
    url(r'^$', views.OrderListView.as_view()),
    url(r'^(?P<pk>\d+)/', views.OrderView.as_view()),
    url(r'^customers/(?P<pk>\d+)/', views.CustomerOrderView.as_view()),
    url(r'^orderlines/$', views.OrderLineListView.as_view()),
    url(r'^orderlines/(?P<pk>\d+)/', views.OrderLineView.as_view()),
    url(r'^orderlines/state/(?P<state>[OLACST])/', views.OrderLineByStateView.as_view()),
    url(r'^orderlinestates/state/(?P<state>[OLACST])/', views.OrderLineStateByStateView.as_view()),
    url(r'^orderlinestates/$', views.OrderLineStateListView.as_view()),
    url(r'^orderlinestates/(?P<pk>\d+)', views.OrderLineStateView.as_view()),
    url(r'^orderlinestates/orderline/(?P<orderline>\d+)', views.OrderLineStateByOrderLineView.as_view()),
]