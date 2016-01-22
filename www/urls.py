"""
WWW URL Configuration
"""

from django.conf.urls import url, include
from www.views import home

urlpatterns = [
    # Home page
    url(r'^$', home, name='home')
]
