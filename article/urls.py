from django.conf.urls import url

from article import views


urlpatterns = [
    url(r'^$', views.ArticleTypeListView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.ArticleTypeView.as_view()),
    url(r'^(?P<article_type>\d+)/suppliers/$', views.ArticleTypeSupplierView.as_view()),
    url(r'^(?P<article_type>\d+)/suppliers/(?P<supplier>\d+)/$', views.UpdateArticleTypeSupplierView.as_view()),

]
