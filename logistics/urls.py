from django.conf.urls import url

from logistics import views

urlpatterns = [
    # Standard page
    url(r'^supplierorder/$', views.SupplierOrderListView.as_view()),

]
