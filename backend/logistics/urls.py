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
    url(r'^supplierorderstate/supplierorderline/(?P<supplier_order_line_pk>\d+)/$', views.SupplierOrderStateBySupplierOrderLineView.as_view()),
    url(r'^stockwish/$', views.StockWishView.as_view()),
    url(r'^stockwishtablelog/$', views.StockWishTableLogListView.as_view()),
    url(r'^stockwishtablelog/(?P<pk>\d+)/$', views.StockWishTableLogView.as_view()),
    url(r'^stockwishtablelog/stockwish/(?P<stock_wish_id>\d+)/$', views.StockWishTableLogViewByStockWish.as_view()),
]
