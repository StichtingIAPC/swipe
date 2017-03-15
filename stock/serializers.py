from stock.models import Stock, StockLabeledLine
from money.serializers import CostSerializerField

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class StockLabeledLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLabeledLine
        fields = ('labeltype',
                  'labelkey')

class StockSerializer(StockLabeledLineSerializer):
    book_value = CostSerializerField()
    class Meta:
        model = Stock
        fields = StockLabeledLineSerializer.Meta.fields + (
            'article',
            'count',
            'book_value'
        )