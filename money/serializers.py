from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from money.models import CurrencyData as Currency, Denomination, \
    AccountingGroup, Money, VAT, VATPeriod, Cost




class MoneySerializerField(serializers.Field):
    def to_internal_value(self, data):
        if data is None:
            return None
        try:
            return Money(amount=Decimal(data['amount']),
                         currency=Currency(data['currency']))
        except Exception as e:
            raise ValidationError from e

    def to_representation(self, obj: Money):
        return {
            'amount': str(obj.amount),
            'currency': obj.currency.iso
        }


class CostSerializerField(MoneySerializerField):
    def to_internal_value(self, data):
        if data is None:
            return None
        try:
            return Cost(amount=Decimal(data['amount']),
                        currency=Currency(data['currency']))
        except Exception as e:
            raise ValidationError from e


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
            'id',
            'accounting_number',
            'vat_group',
            'name',
        )


class VATPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = VATPeriod
        fields = (
            'id',
            'begin_date',
            'end_date',
            'vatrate',
        )


class VATSerializer(serializers.ModelSerializer):
    vatperiod_set = VATPeriodSerializer(many=True)

    class Meta:
        model = VAT
        fields = (
            'id',
            'name',
            'active',
            'vatperiod_set'
        )

    def create(self, validated_data):
        vatperiods = validated_data.pop('vatperiod_set')
        vat = None
        with transaction.atomic():
            vat = VAT.objects.create(**validated_data)
            for vp_data in vatperiods:
                VATPeriod.objects.create(**vp_data, vat=vat)
        return vat

    def update(self, instance: VAT, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        try:
            updateable = instance.vatperiod_set.get(end_date__isnull=True)
        except Exception:
            updateable = {'id': object()}
        new_vps = []
        for vp in validated_data['vatperiod_set']:
            if getattr(updateable, 'id', object()) == vp.get('id'):
                updateable.end_date = vp['end_date']
                updateable.save()
            elif vp.get('id') is not None:
                new_vps.append(VATPeriod(**vp))
        instance.vatperiod_set.add(*new_vps, bulk=False)
        instance.save()
        return instance
