from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from authorization import views


urlpatterns = (
    url(r'login/', views.Login.as_view()),
    url(r'logout/', views.Logout.as_view()),
    url(r'validate/', views.Validate.as_view()),
    url(r'api-token-auth/', obtain_jwt_token)
)
