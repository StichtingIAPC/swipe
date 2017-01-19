from decimal import Decimal

from rest_framework import serializers

from register.models import Register, PaymentType, RegisterCount, RegisterPeriod, DenominationCount


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
    currency = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_type = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_representation(self, instance: Register):
        obj = super().to_representation(instance=instance)
        if instance.is_cash_register:
            obj['denomination_counts'] = None
            return obj
        denom_counts = instance.denomination_counts

        denomination_counts = [{
                'amount': denom_count.denomination.amount,
                'count': denom_count.amount
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


class RegisterCountSerializer(serializers.Serializer):
    register_period = serializers.PrimaryKeyRelatedField(read_only=True)

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
        return data

    def to_internal_value(self, data):
        denomination_counts = data.pop('denomination_counts')
        instance = super().to_internal_value(data)
        period = RegisterPeriod.objects.prefetch_related('register__currency__denomination_set').get(instance.register_period)
        denom_counts = []
        if period.register.is_cash_register:
            denominations = list(period.register.currency.denomination_set.all())
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
            'register_period',
            'is_opening_count',
            'amount',
        )
