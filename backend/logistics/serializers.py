from rest_framework import serializers

from article.serializers import ArticleTypeSerializer
from logistics.models import SupplierOrder, SupplierOrderLine, SupplierOrderState, StockWishTableLog, StockWish
from money.serializers import CostSerializerField
from supplier.serializers import ArticleTypeSupplierSerializer

class SupplierOrderLineSerializer(serializers.ModelSerializer):

    line_cost = CostSerializerField()

    class Meta:
        model = SupplierOrderLine
        fields = (
            'id',
            'supplier_order',
            'article_type',
            'supplier_article_type',
            'order_line',
            'line_cost',
            'state',
        )


class SupplierOrderSerializer(serializers.ModelSerializer):

    supplierorderline_set = SupplierOrderLineSerializer(many=True)

    class Meta:
        model = SupplierOrder
        fields = (
            'id',
            'supplier',
            'supplierorderline_set',
        )


class SupplierOrderStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierOrderState
        fields = (
            'id',
            'timestamp',
            'supplier_order_line',
            'state',
        )


class StockWishSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockWish
        fields = (
            'timestamp',
        )


class StockWishTableLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockWishTableLog
        fields = (
            'number',
            'article_type',
            'supplier_order',
            'stock_wish',
        )

