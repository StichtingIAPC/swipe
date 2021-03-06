from rest_framework import serializers
from externalise.models import ExternaliseDocument, ExternaliseLine
from money.serializers import CostSerializerField
from article.serializers import ArticleTypeSerializer


class ExternaliseLineSerializer(serializers.ModelSerializer):
    cost = CostSerializerField()
    article_type = ArticleTypeSerializer()

    class Meta:
        model = ExternaliseLine
        fields = (
            'id',
            'externalise_document',
            'article_type',
            'count',
            'cost'
        )


class ExternaliseDocumentSerializer(serializers.ModelSerializer):
    externaliseline_set = ExternaliseLineSerializer(many=True)

    class Meta:
        model = ExternaliseDocument
        fields = (
            'id',
            'memo',
            'externaliseline_set'
        )
        depth = 2



