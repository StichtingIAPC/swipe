from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from authorization import views


urlpatterns = (
    url(r'login/', views.Login.as_view()),
    url(r'logout/', views.Logout.as_view()),
    url(r'profile/', views.UserProfile.as_view()),
)
