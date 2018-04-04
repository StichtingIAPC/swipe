from django.conf.urls import url
from refreshtoken.views import RefreshTokenViewSet
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from refreshtoken.routers import router as rt_router

from authorization import views


urlpatterns = (
    url(r'login/', views.Login.as_view()),
    url(r'logout/', views.Logout.as_view()),
    url(r'validate/', views.Validate.as_view()),
    url(r'token-auth/', obtain_jwt_token),
    url(r'token-refresh/', refresh_jwt_token),
    url(r'token-verify/', verify_jwt_token),
    url(r'refresh-token/', RefreshTokenViewSet.as_view({'put': 'create', 'get': 'list'})),
)