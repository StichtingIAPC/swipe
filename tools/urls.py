from django.conf import settings
from django.conf.urls import url

from tools.views import TableView



app_name = 'tools'
urlpatterns = ()

if settings.DEBUG:
    urlpatterns += (
        url(r'^tabletest/$', TableView.as_view(), name="table_view"),
    )
