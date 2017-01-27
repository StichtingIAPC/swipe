from rest_framework import serializers

from assortment.models import AssortmentLabel, AssortmentLabelType, AssortmentUnitType


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssortmentLabel
        fields = (
            'id',
            'value',
            'label_type',
        )


class LabelSerializerWithEdit(LabelSerializer):
    class Meta(LabelSerializer.Meta):

        extra_kwargs = {
            'value': {'read_only': False},
            'label_type': {'read_only': False, 'queryset': AssortmentLabelType.objects.all()}
        }


class LabelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssortmentLabelType
        fields = (
            'id',
            'description',
            'name',
            'unit_type',
        )


class LabelTypeSerializerWithEdit(LabelTypeSerializer):
    class Meta(LabelTypeSerializer.Meta):
        extra_kwargs = {
            'name': {'read_only': False},
            'unit_type': {'read_only': False, 'queryset': AssortmentUnitType.objects.all()},
        }


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssortmentUnitType
        fields = (
            'id',
            'type_long',
            'type_short',
            'value_type',
            'incremental_type',
        )


class UnitTypeSerializerWithEdit(UnitTypeSerializer):
    class Meta(UnitTypeSerializer.Meta):
        extra_kwargs = {
            'type_long': {'read_only': False},
            'type_short': {'read_only': False},
            'value_type': {'read_only': False},
        }
