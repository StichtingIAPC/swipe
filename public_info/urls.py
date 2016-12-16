from django.conf.urls import url

from public_info.views import public_view_router_view


app_name = 'public_info'

urlpatterns = (
    url(r'^(P<random_str>[a-zA-Z0-9+-]{16})/$', public_view_router_view, name='shared'),
)
