from rest_framework import serializers

from sales.models import Payment
from money.serializers import MoneySerializerField


class PaymentSerializer(serializers.ModelSerializer):

    amount = MoneySerializerField()
    class Meta():
        model = Payment
        fields = (
            'id',
            'payment_type',
            'amount',
            'transaction'
        )
