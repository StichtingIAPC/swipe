"""
WWW URL Configuration
"""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from www.views import home

urlpatterns = [
    # Home page
    url(r'^$', home, name='home'),

    # Authentication URLs
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^switch_user/$', auth_views.logout_then_login, name='switch_user'),

    # Include Supplier URLs
    url(r'^supplier/', include('supplier.urls')),
]
