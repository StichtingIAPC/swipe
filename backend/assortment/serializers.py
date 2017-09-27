from rest_framework import serializers

from assortment.models import AssortmentLabel, AssortmentLabelType, AssortmentUnitType


class LabelSerializer(serializers.ModelSerializer):
    """
    shape:
    {
      "id": Number,
      "value": String,
    }
    """
    class Meta:
        model = AssortmentLabel
        fields = (
            'id',
            'value',
        )


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

    def to_internal_value(self, data: dict):
        data.pop('labels')
        return super().to_internal_value(data=data)

    def to_representation(self, instance: AssortmentLabelType):
        _repr = super().to_representation(instance)
        _repr['labels'] = [LabelSerializer().to_representation(label) for label in instance.assortmentlabel_set.all()]
        return _repr


class LabelTypeSerializerWithEdit(LabelTypeSerializer):
    """
    shape:
    {
      "id": Number,
      "description": String,
      "name": String,
      "unit_type": UnitTypeID,
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
      "value_type": chars,
      "incremental_type": chars,
    }
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
      "value_type": chars,
      "incremental_type": chars,
    }
    """
    class Meta(UnitTypeSerializer.Meta):
        extra_kwargs = {
            'type_long': {'read_only': False},
            'type_short': {'read_only': False, 'allow_blank': True},
            'value_type': {'read_only': False},
        }
