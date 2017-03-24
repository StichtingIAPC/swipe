from rest_framework import serializers

from article.models import ArticleType, WishableType
from assortment.models import AssortmentLabel
from money.serializers import MoneySerializerField

def get_or_create_labels(labels_obj):
    """
    :param labels_obj: a dict with labelTypeID's as keys and an array of labelValues as value
    :type labels_obj: {labelTypeID: [labelValues]}
    :return:
    """
    q = Q()
    for labeltype_id, values in labels_obj.items():
        q &= Q(label_type__id=labeltype_id, value__in=values)

    asls = list(AssortmentLabel.objects.filter(q).select_related('label_type').all())

    expected_labels = {(label_value, label_type) for label_type, lvals in labels_obj.items() for label_value in lvals}

    for asl in asls:
        expected_labels.remove((asl.value, asl.label_type.pk))

    for (label_value, label_type_id) in expected_labels:
        asls.append(AssortmentLabel.objects.create(value=label_value, label_type_id=label_type_id))

    return asls


def label_set_to_labels_for(article_type: WishableType):
    labels = {}
    for label in article_type.labels.all():
        lst = labels.get(label.label_type_id)
        if not lst:
            labels[label.label_type_id] = []
        labels[label.label_type_id].append(label.value)
    return labels


class ArticleTypeSerializer(serializers.ModelSerializer):
    fixed_price = MoneySerializerField(allow_null=True)

    class Meta:
        model = ArticleType
        fields = (
            'id',
            'fixed_price',
            'accounting_group',
            'name',
            'ean',
            'serial_number',
        )
        depth = 0

    def to_representation(self, instance):
        _repr = super().to_representation(instance=instance)
        _repr['labels'] = label_set_to_labels_for(instance)
        return _repr

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def create(self, validated_data):
        labels = validated_data.pop('labels')

        art = ArticleType.objects.create(**validated_data)

        art.labels.set(get_or_create_labels(labels))

        return art

    def update(self, instance, validated_data):
        instance.fixed_price = validated_data.get('fixed_price', instance.fixed_price)
        instance.accounting_group = validated_data.get('accounting_group', instance.accounting_group)
        instance.name = validated_data.get('name', instance.name)

        if validated_data.get('labels'):
            labels = get_or_create_labels(validated_data.get('labels'))

            instance.labels.set(labels)

        instance.save()
        return instance
