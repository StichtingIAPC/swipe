from django.conf.urls import url

from sales import views

urlpatterns = [
    # Standard page
    url(r'^payments/(?P<pk>\d+)/$', views.PaymentView.as_view(), name="payment_view"),
    url(r'^payments/$', views.PaymentListView.as_view(), name="paymentopenlist_view"),
    url(r'^payments/list/(?P<pk>\d+)/$', views.PaymentGroupView.as_view(), name="paymentgroup_view"),
    url(r'^payments/list/opened/$', views.PaymentGroupOpenedView.as_view(), name="paymentgroupopened_view"),
    url(r'^payments/opened/$', views.PaymentOpenListView.as_view(), name="paymentopenlist_view"),
    url(r'^payments/totals/(?P<pk>\d+)/$', views.PaymentTotalsView.as_view(), name="paymenttotals_view"),
    url(r'^payments/totals/latest/$', views.PaymentsLatestTotalsView.as_view(), name="paymentlatesttotals_view"),
    url(r'^transactions/$', views.TransactionListView.as_view(), name="transaction_view"),
    url(r'^transactions/create/$', views.TransactionCreateView.as_view(), name="transactioncreate_view"),
    url(r'^transactions/opened/$', views.TransactionOpenView.as_view(), name="transactionopenlist_view"),
    url(r'^transactions/(?P<pk>\d+)/$', views.TransactionView.as_view(), name="transactionlist_view"),


]
