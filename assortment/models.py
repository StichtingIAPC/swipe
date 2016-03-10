import re


import math

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db import models

from assortment.config import labels as conf_labels


"""
From here on: Tags

Tags will be used as the main way to generate a tree. Other components that can be used will be labels, but labels are
a lot more complex to generate a tree from, so we pre-build the trunk from tags.
"""


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent_tag = models.ForeignKey('Tag', blank=True, null=True)

    class Meta:
        pass


"""
From here on: Labels
"""


class Label(models.Model):
    value = models.TextField(max_length=64, editable=False)
    label_type = models.ForeignKey('LabelType', on_delete=models.CASCADE, editable=False)

    @classmethod
    def get_or_create(cls, value, label_type):
        if not isinstance(value, str):
            raise AssertionError('initial label_value must be of type str')

        obj, new = cls.objects.get_or_create(value=value, label_type=label_type)

        obj._value = label_type.unit_type.parse(value)
        obj.label_value = str(obj._value)
        obj.save()
        return obj, new

    def __str__(self):
        return self.label_type.to_string(self._value)

    class Meta:
        ordering = ['label_type', 'value']
        unique_together = (
            ('value', 'label_type'),
        )


class LabelType(models.Model):
    name_long = models.CharField(max_length=64, unique=True)
    # a longer description of what this type of label does, e.g. 'the length of a cable'
    name_short = models.CharField(max_length=16, unique=True, editable=False)
    # the short representation that should be visible on the label, e.g. 'length'
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, editable=False)
    # the unittype this label uses

    def to_string(self, value, *args, shortened=True):
        return "{}: {}{}".format(
            self.name_short,
            self.value_to_string(value, shortened),
            self.unit_type.type_short if shortened else self.unit_type.type_long)

    def value_to_string(self, value, shortened=True):
        if (self.unit_type.counting_type in conf_labels.NON_COUNTABLE_ENUMERATION_TYPES or
                self.unit_type.incremental_type is None):
            return str(value)

        incr_settings = conf_labels.SYMBOL_EXTENDED[self.unit_type.incremental_type]
        # get the settings of the incrementation
        rel_value = value / incr_settings['start']
        # get the value relative to the start of the list
        index = math.floor(math.log(rel_value, int(incr_settings['factor'])))
        # calculate the index that the corresponding string is stored

        if index < 0 or index > len(incr_settings['values']):
            return str(value)

        value_representation = rel_value / math.pow(int(incr_settings['factor']), index)
        value_symbol, value_symbol_extended = list(incr_settings['values'])[index]

        return "{} {}{}".format(
            type(value)(value_representation),
            value_symbol if shortened else value_symbol_extended,
            incr_settings['seperator']
        )

    def label(self, val):
        value = self.unit_type.parse(str(val))
        obj, new = Label.get_or_create(value=str(value), label_type=self)
        return obj


class UnitType(models.Model):
    type_short = models.CharField(max_length=8, editable=False)  # e.g. 'm' for meters, 'l' for liters
    type_long = models.CharField(max_length=255, editable=False)    # e.g. 'meter' or 'liter'
    counting_type = models.CharField(max_length=1, choices=conf_labels.ENUMERATION_TYPES, editable=False)
    # is it a string, an integer, a decimal or a boolean?
    incremental_type = models.CharField(max_length=3, choices=conf_labels.SYMBOL_TYPES, blank=True, null=True)
    # in case of integer or decimal, do you want it to be visualized in powers of something, like millions, billions,
    # mega, mini, milliards, etc?

    def __str__(self):
        if self.incremental_type:
            return _("{} seen as {} using type {} and formatted using {}".format(
                self.type_long,
                self.type_short,
                self.get_counting_type_display(),
                self.incremental_type
            ))
        else:
            return _("{} seen as {} using type {}".format(
                self.type_long,
                self.type_short,
                self.get_counting_type_display()
            ))

    def parse(self, value):
        return conf_labels.ENUMERATION_PARSERS[self.counting_type](value)

    def clean(self):
        if self.counting_type in conf_labels.NON_COUNTABLE_ENUMERATION_TYPES and self.incremental_type:
            # string type etc.
            raise ValidationError('When the type of the unit is not countable, '
                                  'you cannot have an incremental_type specified')

    class Meta:
        ordering = ['type_short', 'type_long']
        unique_together = (
            ('type_short', 'counting_type'),
            ('type_long', 'counting_type')
        )
