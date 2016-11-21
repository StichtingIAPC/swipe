from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from authorization import views


urlpatterns = (
    url(r'login/', obtain_auth_token),
    url(r'logout/', views.logout),
)
