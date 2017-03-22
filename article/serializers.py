from rest_framework import serializers

from article.models import ArticleType
from assortment.models import AssortmentLabel
from money.serializers import MoneySerializerField


class ArticleTypeSerializer(serializers.ModelSerializer):
    fixed_price = MoneySerializerField(allow_null=True)

    class Meta:
        model = ArticleType
        fields = (
            'id',
            'fixed_price',
            'accounting_group',
            'name',
            'labels',
            'ean',
            'serial_number',
        )
        depth = 0

    def create(self, validated_data):
        labels = validated_data.pop('labels')
        art = ArticleType.objects.create(**validated_data)
        art.labels.set(AssortmentLabel.objects.filter(pk__in=labels))
        return art

    def update(self, instance, validated_data):
        instance.fixed_price = validated_data.get('fixed_price', instance.fixed_price)
        instance.accounting_group = validated_data.get('accounting_group', instance.accounting_group)
        instance.name = validated_data.get('name', instance.name)
        if validated_data.get('labels'):
            instance.labels.set(AssortmentLabel.objects.filter(pk__in=validated_data.get('labels')))
        instance.save()
        return instance
