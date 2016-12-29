from money.serializers import DenominationSerializer
from rest_framework import serializers

from register.models import Register, RegisterCount, PaymentType, RegisterPeriod, DenominationCount, SalesPeriod


class PaymentTypeSerializer(serializers.ModelSerializer):
    """
    result: {
      "name": "string",
      "closing_memo": "string"
    }
    """
    class Meta:
        model = PaymentType
        fields = (
            'name',
            'is_invoicing',
        )


class SalesPeriodSerializer(serializers.ModelSerializer):
    """
    result: {
      "beginTime": "<Time>",
      "endTime": "<Time>",
      "closing_memo": "string"
    }
    """
    class Meta:
        model = SalesPeriod
        fields = (
            'beginTime',
            'endTime',
            'closing_memo',
        )


class DenominationCountSerializer(serializers.Serializer):
    """
    result: {
      "register_count": <RegisterCount>,
      "denomination": <Denomination>,
      "amount": Number,
    }
    """
    denomination = DenominationSerializer()

    class Meta:
        model = DenominationCount
        fields = (
            'denomination',
            'amount',
        )


class RegisterCountSerializer(serializers.Serializer):
    """
    result: {
      "is_opening_count": Boolean,
      "amount": Number
    }
    """
    denominationcount_set = DenominationCountSerializer(many=True)

    class Meta:
        model = RegisterCount
        field = (
            'is_opening_count',
            'amount',
            'denominationcount_set',
        )


class RegisterPeriodSerializer(serializers.Serializer):
    """
    result: {
      "sales_period": <SalesPeriod.ID>,
      "registercount_set": [<RegisterCount>] | [<RegisterCount>, <RegisterCount>],
      "beginTime": "<Time>",
      "endTime": "<Time>",
      "memo": String,
    }
    """
    sales_period = serializers.PrimaryKeyRelatedField(read_only=True)
    registercount_set = RegisterCountSerializer(many=True, read_only=True)

    class Meta:
        model = RegisterPeriod
        fields = (
            'sales_period',
            'beginTime',
            'endTime',
            'memo',
            'registercount_set',  # reverse field for register counts
        )


class RegisterSerializer(serializers.ModelSerializer):
    """
    result: {
      "name": String,
      "currency": <Currency.ISO>,
      "is_cash_register": Boolean,
      "is_active": Boolean,
      "payment_type": <PaymentType.PK>,
      "registerperiod_set": [<RegisterPeriod>...]
    }
    """
    currency = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_type = serializers.PrimaryKeyRelatedField(read_only=True)
    registerperiod_set = RegisterPeriodSerializer(many=True, read_only=True)

    class Meta:
        model = Register
        fields = (
            'name',
            'currency',
            'is_cash_register',
            'is_active',
            'payment_type',
            'registerperiod_set',
        )
