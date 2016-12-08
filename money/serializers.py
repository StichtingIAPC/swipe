from rest_framework import serializers

from money.models import CurrencyData as Currency, Denomination, AccountingGroup


class DenominationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denomination
        fields = (
            'id',
            'amount',
        )


class CurrencySerializer(serializers.ModelSerializer):
    denomination_set = DenominationSerializer(many=True)

    class Meta:
        model = Currency
        fields = (
            'iso',
            'name',
            'digits',
            'symbol',
            'denomination_set'
        )
        depth = 1

    def create(self, validated_data):
        denomination_data = validated_data.pop('denomination_set')
        currency = Currency.objects.create(**validated_data)
        for denom in denomination_data:
            Denomination.objects.create(currency=currency, **denom)
        return currency

    def update(self, instance, validated_data):
        instance.iso = validated_data.get('iso', instance.iso)
        instance.name = validated_data.get('name', instance.name)
        instance.digits = validated_data.get('digits', instance.digits)
        instance.symbol = validated_data.get('symbol', instance.symbol)

        if validated_data.get('denomination_set') is not None:  # can be [] in case all denominations are deleted
            denoms = []
            for denom in validated_data.get('denomination_set'):
                try:
                    denoms.append(instance.denomination_set.get(amount=denom.get('amount')))
                except Denomination.DoesNotExist as e:
                    denoms.append(instance.denomination_set.create(amount=denom.get('amount')))
            instance.denomination_set.set(denoms)
        return instance


class AccountingGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountingGroup
        fields = (

        )