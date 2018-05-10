from rest_framework import generics
from rest_framework import mixins

from article.models import ArticleType
from article.serializers import ArticleTypeSerializer
from supplier.models import ArticleTypeSupplier
from supplier.serializers import ArticleTypeSupplierSerializer
from tools.json_parsers import ParseError
from www.models import SwipeLoginRequired


class ArticleTypeListView(SwipeLoginRequired, mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleTypeView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UpdateArticleTypeSupplierView(SwipeLoginRequired, mixins.UpdateModelMixin,
                                    generics.GenericAPIView):
    serializer_class = ArticleTypeSupplierSerializer

    lookup_field = 'supplier'

    def get_queryset(self):
        return ArticleTypeSupplier.objects.filter(article_type=self.kwargs["article_type"],
                                                  supplier=self.kwargs["supplier"])

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ArticleTypeSupplierView(SwipeLoginRequired, mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):
    serializer_class = ArticleTypeSupplierSerializer

    def get_queryset(self):
        return ArticleTypeSupplier.objects.filter(article_type=self.kwargs["article_type"])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
