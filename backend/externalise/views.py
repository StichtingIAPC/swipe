import json
from decimal import Decimal

from django.http import HttpResponse
from rest_framework import mixins, generics

from article.models import ArticleType
from crm.models import User
from externalise.models import ExternaliseDocument, IncorrectClassError
from externalise.serializers import ExternaliseDocumentSerializer
from money.models import Cost
from tools.util import raiseif


class ExternaliseDocumentView(mixins.RetrieveModelMixin,
                              generics.GenericAPIView):
    queryset = ExternaliseDocument.objects.all()
    serializer_class = ExternaliseDocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ExternaliseRequest:

    def __init__(self, user: int, article_information_list: list, memo: str):
        raiseif(not isinstance(user, int), IncorrectClassError)
        self.user = user
        self.article_information = []
        for information in article_information_list:
            self.article_information.append(ExternaliseRequest.ArticleInformation(
                article=information.get("article"), count=information.get("count"),
                cost=information.get("cost")
            ))
        raiseif(not isinstance(memo, str), IncorrectClassError)
        self.memo = memo

    def create_externalise_document(self):
        user = User.objects.get(pk=self.user)
        art_info = []
        for art in self.article_information:
            art_info.append(art.to_model_data())
        return ExternaliseDocument.create_external_products_document(user=user,
                                                                     article_information_list=art_info,
                                                                     memo=self.memo)

    class ArticleInformation:

        def __init__(self, article: int, count: int, cost):
            self.article = article
            raiseif(not isinstance(article, int), IncorrectClassError)
            self.count = count
            raiseif(not isinstance(count, int), IncorrectClassError)
            self.cost = cost

        def to_model_data(self):
            article = ArticleType.objects.get(pk=self.article)
            amnt = self.cost.get("amount")
            cost = Cost(amount=Decimal(amnt), use_system_currency=True)
            return (article, self.count, cost)


class ExternaliseDocumentListView(mixins.ListModelMixin,
                                  generics.GenericAPIView):
    queryset = ExternaliseDocument.objects.all()
    serializer_class = ExternaliseDocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request):
        externalise_request = ExternaliseRequest(user=request.data.get("user"),
                                                 article_information_list=request.data.get("externaliseline_set"),
                                                 memo=request.data.get("memo"))
        externalise_representation = ExternaliseDocumentSerializer(instance=externalise_request.create_externalise_document()).data
        return HttpResponse(content=json.dumps(externalise_representation), content_type="application/json")