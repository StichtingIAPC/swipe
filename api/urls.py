from django.conf.urls import url, include


urlpatterns = [
    url(r'^assortment/',
        include('assortment.api_urls'),
        name='assortment',
        prefix='assortment'),
]
