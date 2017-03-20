from stock.models import Stock, StockLabeledLine
from money.serializers import CostSerializerField, MoneySerializerField
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

    class CustomArticleSerializer(serializers.RelatedField):
        def to_representation(self, value: ArticleType):
            fp=value.fixed_price
            if fp:
                return {'id': value.pk, 'fixed_price': {'amount': fp.amount, 'currency': fp.currency.iso}}
            else:
                return {'id': value.pk, 'fixed_price': None}

    article = CustomArticleSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = StockLabeledLineSerializer.Meta.fields + (
            'article',
            'count',
            'book_value',
        )