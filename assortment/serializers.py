from rest_framework import serializers

from assortment.models import AssortmentLabel, AssortmentLabelType, AssortmentUnitType


class LabelSerializer(serializers.ModelSerializer):
    """
    shape:
    {
      "id": Number,
      "value": String,
      "label_type": Number,
    }
    """
    class Meta:
        model = AssortmentLabel
        fields = (
            'id',
            'value',
            'label_type',
        )


class LabelSerializerWithEdit(LabelSerializer):
    """
    shape:
    {
      "id": Number,
      "value": String,
      "label_type": Number,
    }
    """
    class Meta(LabelSerializer.Meta):
        extra_kwargs = {
            'value': {'read_only': False},
            'label_type': {'read_only': False, 'queryset': AssortmentLabelType.objects.all()}
        }


class LabelTypeSerializer(serializers.ModelSerializer):
    """
    shape:
    {
      "id": Number,
      "description": String,
      "name": String,
      "unit_type": Number,
    }
    """
    class Meta:
        model = AssortmentLabelType
        fields = (
            'id',
            'description',
            'name',
            'unit_type',
        )


class LabelTypeSerializerWithEdit(LabelTypeSerializer):
    """
    shape:
    {
      "id": Number,
      "description": String,
      "name": String,
      "unit_type": Number,
    }
    """

    class Meta(LabelTypeSerializer.Meta):
        extra_kwargs = {
            'name': {'read_only': False},
            'unit_type': {'read_only': False, 'queryset': AssortmentUnitType.objects.all()},
        }


class UnitTypeSerializer(serializers.ModelSerializer):
    """
    shape:
    {
      "id": Number,
      "type_long": String,
      "type_short": String,
      "value_type": String,
      "incremental_type": String,
    """
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
    """
    shape:
    {
      "id": Number,
      "type_long": String,
      "type_short": String,
      "value_type": String,
      "incremental_type": String,
    """
    class Meta(UnitTypeSerializer.Meta):
        extra_kwargs = {
            'type_long': {'read_only': False},
            'type_short': {'read_only': False},
            'value_type': {'read_only': False},
        }
