from rest_framework import serializers

from money.serializers import SalesPriceSerializer
from order.models import Order, OrderLine, OrderLineState

class OrderLineSerializer(serializers.ModelSerializer):
    expected_sales_price = SalesPriceSerializer()
    final_sales_price = SalesPriceSerializer()

    class Meta:
        model = OrderLine
        fields = (
            'id',
            'order',
            'wishable',
            'state',
            'expected_sales_price',
            'final_sales_price'
        )


class OrderSerializer(serializers.ModelSerializer):
    orderline_set = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'notes',
            'orderline_set'
        )
        # depth = 1


class OrderLineStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLineState
        fields = (
            'id',
            'state',
            'timestamp',
            'orderline'
        )