from rest_framework import serializers

from article.serializers import ArticleTypeSerializer
from logistics.models import SupplierOrder, SupplierOrderLine
from supplier.serializers import ArticleTypeSupplierSerializer


class SupplierOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierOrder
        fields = (
            'supplier'
        )


class SupplierOrderLineSerializer(serializers.ModelSerializer):

    supplier_order = SupplierOrderSerializer()
    article_type = ArticleTypeSerializer()
    supplier_article_type = ArticleTypeSupplierSerializer()

    class Meta:
        model = SupplierOrderLine
        fields = (
            'supplier_order',
            'article_type',
            'supplier_article_type',
            'order_line',
            'line_cost',
            'state'
        )
