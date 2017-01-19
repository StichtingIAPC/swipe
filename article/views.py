# Create your views here.
from rest_framework import generics
from rest_framework import mixins

from article.models import ArticleType
from article.serializers import ArticleTypeSerializer


class ArticleListView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):

    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)


class ArticleTypeView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):

    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request=request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)
