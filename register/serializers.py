from decimal import Decimal

from django.db.models import Sum, Field
from rest_framework import serializers

from money.serializers import MoneySerializerField
from register.models import Register, PaymentType, RegisterCount, DenominationCount, SalesPeriod
from sales.models import TransactionLine


class PaymentTypeSerializer(serializers.ModelSerializer):
    """
    result: {
      "id": Integer,
      "name": String,
      "is_invoicing": Boolean
    }
    """
    class Meta:
        model = PaymentType
        fields = (
            'id',
            'name',
            'is_invoicing',
        )


class RegisterSerializer(serializers.ModelSerializer):
    """
    result: {
      "id": Integer
      "name": String,
      "currency": Currency.ISO,
      "is_cash_register": Boolean,
      "is_active": Boolean,
      "payment_type": PaymentType.PK
    }
    """

    def to_representation(self, instance: Register):
        obj = super().to_representation(instance=instance)
        if not instance.is_cash_register:
            obj['denomination_counts'] = None
            return obj
        denom_counts = instance.denomination_counts

        denomination_counts = [{
                'amount': denom_count.denomination.amount,
                'count': denom_count.number
            } for denom_count in denom_counts
        ]
        obj['denomination_counts'] = denomination_counts
        return obj

    def to_internal_value(self, data):
        denomination_counts = data.pop('denomination_counts', [])
        obj = super().to_internal_value(data)
        return obj

    class Meta:
        model = Register
        fields = (
            'id',
            'name',
            'currency',
            'is_cash_register',
            'is_active',
            'payment_type',
        )


class RegisterCountSerializer(serializers.ModelSerializer):
    """
    shape: {
      "id": RegisterCount.PK,
      "register": Register.PK
      "is_opening_count": Boolean,
      "amount": Optional<"Decimal">,
      "currency": CurrencyData
      "denomination_counts": Array<{
        "amount": "Decimal",
        "number": Number,
      }>,
    }
    """

    def to_representation(self, instance: RegisterCount):
        data = super().to_representation(instance=instance)
        denom_counts = None

        if instance.is_cash_register_count():
            denom_counts = []
            for denom_count in instance.denominationcount_set.all().select_related('denomination'):
                denom_counts.append({
                    'amount': denom_count.denomination.amount,
                    'number': denom_count.number
                })

        data['denomination_counts'] = denom_counts
        data['currency'] = instance.register.currency_id
        data['register'] = instance.register_id
        return data

    def to_internal_value(self, data):
        denomination_counts = data.pop('denomination_counts')
        instance = super().to_internal_value(data)
        denom_counts = []
        if instance.register.is_cash_register:
            denominations = list(instance.register.currency.denomination_set.all())
            for denom in denominations:
                number = 0

                for denom_count in denomination_counts:
                    if Decimal(denom_count['amount']) == denom.amount:
                        number = denom_count['number']
                        break

                denom_counts.append(DenominationCount(
                    register_count=instance,
                    denomination=denom,
                    number=number
                ))
            instance.denominationcount_set.set(denom_counts)

        return instance

    class Meta:
        model = RegisterCount
        fields = (
            'id',
            'is_opening_count',
            'amount',
        )


class OpeningCountDifferenceSerializer(serializers.Serializer):
    difference = MoneySerializerField()
    register = serializers.IntegerField()


class ClosingCountDifferenceSerializer(serializers.Serializer):
    difference = MoneySerializerField


class RegisterClosingSerializer(serializers.Serializer):
    def to_internal_value(self, data: dict):
        serializer = RegisterCountSerializer()
        res = {}
        for key, value in data.items():
            res[int(key)] = serializer.to_internal_value( value)
        return res


class SalesPeriodSerializer(serializers.ModelSerializer):
    """
    shape: {
      "id": SalesPeriod.PK,
      "beginTime": "DateTime",
      "endTime": "DateTime",
      "money_differences": Array<{
        "currency": "Currency.ISO",
        "amount": "Decimal",
      }>
    }
    """
    registercount_set = RegisterCountSerializer(many=True)
    closingcountdifference_set = ClosingCountDifferenceSerializer(many=True)

    def to_internal_value(self, data: dict):
        data.pop('money_differences', None)
        return super().to_internal_value(data)

    def to_representation(self, instance: SalesPeriod):
        _repr = super().to_representation(instance)
        _repr['money_differences'] = TransactionLine.objects\
            .filter(transaction__salesperiod=instance)\
            .order_by('price_currency')\
        #    .annotate(amount=Sum('price'), currency=Field('price_currency'))\
        #    .values('amount', 'currency')
        return _repr

    class Meta:
        model = SalesPeriod
        fields = (
            'id',
            'beginTime',
            'endTime',
            'registercount_set',
            'closingcountdifference_set',
        )
