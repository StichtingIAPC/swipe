from rest_framework import generics
from rest_framework import mixins

from article.models import ArticleType
from article.serializers import ArticleTypeSerializer
from tools.json_parsers import ParseError


class ArticleDictParsers:

    @staticmethod
    def article_parser(obj: int):
        if not obj:
            raise ParseError("Article does not exist")
        if not isinstance(obj, int):
            raise ParseError("Article is not an int")
        return ArticleType.objects.get(id=obj)

class ArticleTypeListView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleTypeView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
