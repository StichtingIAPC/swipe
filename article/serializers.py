from rest_framework import serializers

from article.models import ArticleType


class ArticleTypeSerializer(serializers.Serializer):
    class Meta:
        model = ArticleType
        fields = (
            'id',
            'fixed_price',
            'accounting_group',
            'name',
            'labels',
        )
