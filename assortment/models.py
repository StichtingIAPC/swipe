from django.db import models


COUNTING_TYPES = (
    ('s', 'string'),
    ('n', 'number'),
    ('i', 'integer'),
    ('b', 'boolean'),
)


class Label(models.Model):
    value = models.TextField(max_length=64)
    label_type = models.ForeignKey('LabelType', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.label_type.value_to_string(self.value)

    class Meta:
        ordering = ['label_type', 'value']
        unique_together = (
            ('value', 'label_type'),
        )


class LabelType(models.Model):
    name_long = models.CharField(max_length=64, unique=True)
    # a longer description of what this type of label does, e.g. 'cable length'
    name_short = models.CharField(max_length=16, unique=True)
    # the short representation that should be visible on the label, e.g. 'length'
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, blank=False, null=False)
    # the unittype this label uses

    def value_to_string(self, value):
        return "{}: {}{}".format(self.name_short, value, self.unit_type.type_short)

    def label(self, val):
        value = self.unit_type.parse(val)
        return Label.objects.get_or_create(value=value, label_type=self.pk)


class UnitType(models.Model):
    type_short = models.CharField(max_length=32, unique=True)
    type_long = models.CharField(max_length=2, unique=True)
    counting_type = models.CharField(max_length=1, choices=COUNTING_TYPES)

    def __str__(self):
        return "{} seen as {} using type {}".format(self.type_long, self.type_short, self.get_counting_type_display())

    class Meta:
        ordering = ['type_short', 'type_long']
