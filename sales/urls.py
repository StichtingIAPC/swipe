from django.conf.urls import url

from sales import views

urlpatterns = [
    # Standard page
    url(r'^payments/(?P<pk>\d+)/$', views.PaymentView.as_view(), name="payment_view"),
    url(r'^payments/', views.PaymentListView.as_view(), name="paymentopenlist_view"),
    url(r'^payments/opened/', views.PaymentOpenListView.as_view(), name="paymentopenlist_view"),
    url(r'^transactions/(?P<pk>\d+)/', views.TransactionView.as_view(), name="transaction_view")
]
