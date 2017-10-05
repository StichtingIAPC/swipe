from django.conf.urls import url

from logistics import views

urlpatterns = [
    # Standard page
    url(r'^supplierorder/$', views.SupplierOrderListView.as_view()),
    url(r'^supplierorder/(?P<pk>\d+)/$', views.SupplierOrderView.as_view()),
    url(r'^supplierorderline/$', views.SupplierOrderLineListView.as_view()),
    url(r'^supplierorderline/(?P<pk>\d+)/$', views.SupplierOrderLineView.as_view()),
    url(r'^supplierorderstate/$', views.SupplierOrderStateListView.as_view()),
    url(r'^supplierorderstate/(?P<pk>\d+)/$', views.SupplierOrderStateView.as_view()),
    url(r'^supplierorderstate/state/(?P<state>[OLACST])/', views.SupplierOrderStateByStateView.as_view()),
    url(r'^stockwishtablelog/$', views.StockWishTableLogView.as_view()),
]
