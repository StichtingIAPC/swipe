from rest_framework import serializers

from money.serializers import CostSerializerField
from supplier.models import Supplier, ArticleTypeSupplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            'id',
            'name',
            'search_url',
            'notes',
            'is_used',
            'is_backup',
        )


class ArticleTypeSupplierSerializer(serializers.ModelSerializer):
    cost = CostSerializerField()

    class Meta:
        model = ArticleTypeSupplier
        fields = (
            'supplier',
            'article_type',
            'cost',
            'minimum_number_to_order',
            'supplier_string',
            'availability',
        )

