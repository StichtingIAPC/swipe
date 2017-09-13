from django.conf.urls import url

from order import views

urlpatterns = [
    # Standard page
    url(r'^$', views.OrderListView.as_view()),
    url(r'^(?P<pk>\d+)/', views.OrderView.as_view()),
    url(r'^customers/(?P<pk>\d+)/', views.CustomerOrderView.as_view()),
    url(r'^orderlines/$', views.OrderLineListView.as_view()),
]