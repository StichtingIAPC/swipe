from django.conf.urls import url


app_name = 'urlshare'

urlpatterns = (
    url(r'(P<random_str>[a-zA-Z0-9\+-]{16})/', None, name='shared')
)
