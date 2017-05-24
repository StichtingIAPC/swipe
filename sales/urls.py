from django.conf.urls import url

from sales import views

urlpatterns = [
    # Standard page
    url(r'^$', views.PaymentListView.as_view(), name="paymentlist_view")

]
