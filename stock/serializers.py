from crm.models import Customer
from pricing.models import PricingModel
from stock.models import Stock, StockLabeledLine
from money.serializers import CostSerializerField, MoneySerializerField, PriceSerializer
from article.models import ArticleType


from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class StockLabeledLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLabeledLine
        fields = ('labeltype',
                  'labelkey')

class StockSerializer(StockLabeledLineSerializer):
    book_value = CostSerializerField()

    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = Customer.objects.get(id=customer) if customer else None

    class Meta:
        model = Stock
        fields = StockLabeledLineSerializer.Meta.fields + (
            'article',
            'count',
            'book_value',
        )

    def to_representation(self, instance: Stock):
        _repr = super().to_representation(instance)
        _repr['price'] = PriceSerializer().to_representation(PricingModel.return_price(instance.article, customer=self.customer, stock=instance))
        return _repr
