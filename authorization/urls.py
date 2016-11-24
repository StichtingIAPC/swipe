from django.conf.urls import url

from authorization import views


urlpatterns = (
    url(r'login/', views.Login.as_view()),
    url(r'logout/', views.logout),
)
