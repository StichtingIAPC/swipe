"""
This file contains the models that are used to index, sort and model the assortment pages.
"""

import math
import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from assortment.config import labels as conf_labels


class AssortmentLabel(models.Model):
    """
    Labels are THE way to give products properties other than standard properties like price. If you want your
    CPU to have a clockspeed: Label it. If you want your HDD to have a capacity: Label it.
    """
    value = models.TextField(max_length=64, editable=False)
    label_type = models.ForeignKey('AssortmentLabelType', on_delete=models.CASCADE, editable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__value = None

    @property
    def typed_value(self):
        """
        The value of the AssortmentLabel, but then as the type specified by its label type
        :return: the value as a more specific type
        """
        if not self.__value:
            self.__value = None
        return self.__value

    @typed_value.setter
    def typed_value(self, value):
        """
        set the typed value
        :param value: the value it has to be set to, either in the correct type or as a string.
        """
        if self.__value is not None and not isinstance(value, type(self.__value)):
            if type(value) is str:
                self.__value = self.label_type.unit_type.parse(value)
            else:
                raise ValidationError('The given type is not of the correct type')
        else:
            self.__value = value

    @classmethod
    def get(cls, value, label_type):
        """
        The method that is used to get a label with the given LabelType/value-combination. If it does not exist, it
        creates one with the given values.
        :param value: the value of the expected label
        :param label_type: the labeltype of the expected label
        :return: a label with the requested values
        """
        if not isinstance(value, str):
            raise AssertionError('initial label_value must be of type str')

        obj, new = cls.objects.get_or_create(value=value, label_type=label_type)

        obj.typed_value = label_type.unit_type.parse(value)
        obj.label_value = str(obj.typed_value)
        obj.save()
        return obj

    def __str__(self):
        return self.label_type.value_to_string(self.typed_value)

    def __eq__(self, other):
        if isinstance(other, AssortmentLabel):
            return self.label_type == other.label_type and self.typed_value == other.typed_value
        return False

    class Meta:
        ordering = ['label_type', 'value']
        unique_together = (
            ('value', 'label_type'),
        )


"""
Here be LabelTypes
"""


class AssortmentLabelType(models.Model):
    """
    This is used to group labels with the same properties, but different values, together. Like cables:
    they do not all have the same length, but they do all have the property 'length', which is the type of
    the label.
    """
    description = models.CharField(max_length=64, unique=True)
    # a longer description of what this type of label does, e.g. 'the length of a cable'
    name = models.CharField(max_length=16, unique=True, editable=False)
    # the short representation that should be visible on the label, e.g. 'length'
    unit_type = models.ForeignKey('AssortmentUnitType', on_delete=models.CASCADE, editable=False)
    # the unittype this label uses

    def value_to_string(self, value, shortened=True):
        """
        Make a string from a label of which the value is given.
        E.G. a value 3000 may be parsed to 'weight: 3 kg' (shortened) or 'weight: 3 kilogram' (not shortened)

        :param value: the value to be used
        :param shortened: whether or not it should be using the short-handed method
        :return: a string containing the parsed value, using this LabelType as a template
        """
        return "{}: {}".format(
            self.name,
            self.unit_type.value_to_string(value, shortened)
        )

    def label(self, val):
        """
        make a label which has this label type.
        :param val: the expected value of the label
        :return: a label which has this as the label type associated.
        """
        value = self.unit_type.parse(str(val))
        obj = AssortmentLabel.get(value=str(value), label_type=self)
        return obj


class AssortmentUnitType(models.Model):
    """
    UnitType contains several definitions of what measurable dimension a label type is made of. The currently available
    types are string ('s'), integer ('i'), Decimal (number, 'n') and boolean ('b'). You can name the type of value you
    expect, like 'meters', 'seconds', anything really.
    """
    type_short = models.CharField(max_length=8, editable=False)  # e.g. 'm' for meters, 'l' for liters
    type_long = models.CharField(max_length=255, editable=False)    # e.g. 'meter' or 'liter'
    value_type = models.CharField(max_length=1,
                                  choices=sorted([enum['as_choice'] for n, enum in conf_labels.VALUE_TYPES.items()]),
                                  editable=False)
    # is it a string, an integer, a decimal or a boolean?
    incremental_type = models.CharField(max_length=3,
                                        choices=sorted(
                                            [c_type['as_choice'] for m, c_type in conf_labels.COUNTING_TYPES.items()]),
                                        blank=True,
                                        null=True)
    # in case of integer or decimal, do you want it to be visualized in powers of something, like millions, billions,
    # mega, mini, milliards, etc?

    def __init__(self, *args, **kwargs):
        if kwargs.get('value_type') == '':
            kwargs.pop('value_type')
        if kwargs.get('incremental_type') == '':
            kwargs.pop('incremental_type')
        if (kwargs.get('value_type') is not None and
                not conf_labels.VALUE_TYPES[kwargs.get('value_type')]['countable'] and
                kwargs.get('incremental_type') is not None):
            raise ValidationError('You cannot create an AssortmentUnitType of which the value_type is not countable '
                                  'and specify an incremental_type')
        super().__init__(*args, **kwargs)

    def __str__(self):
        if self.incremental_type:
            return _("AssortmentUnitType<{} ({}) [{} {}]>".format(
                self.type_long,
                self.type_short,
                self.get_incremental_type_display(),
                self.incremental_type
            ))
        else:
            return _("AssortmentUnitType<{} ({}) [{}]>".format(
                self.type_long,
                self.type_short,
                self.get_incremental_type_display()
            ))

    def parse(self, value):
        """
        parse the string value given to the value of the
        :param value: the string value that is to be parsed to the correct type
        :return: the parsed value
        :raises: AssertionError: when the string does not match the expected regex
        """
        vtype = conf_labels.VALUE_TYPES[self.value_type]
        if re.match(vtype['matcher'], value):
            return vtype['type'](value)
        else:
            raise vtype['error']

    def value_to_string(self, value, shortened=True):
        """
        Parse the value to a string, taking into account the counting type of this labeltype.
        E.G. value 3000 may be parsed to '3 k' (shortened) or '3 kilo' (not shortened).

        :param value: the natural value to be parsed to a string
        :param shortened: whether or not it should be shortened to a short-handed value
        :return: a string containing the parsed value
        """
        if (self.value_type in
                [enum['as_choice'][1] for a, enum in conf_labels.VALUE_TYPES.items() if enum['countable'] is False] or
                self.incremental_type is None):
            return str(value)
        _value = value
        if type(value) is str:
            if ',' in value or '.' in value:
                value = Decimal(value)
            else:
                value = int(value)
        if value is None:
            value = 0
        incr_settings = conf_labels.COUNTING_TYPES[self.incremental_type]
        # get the settings of the incrementation of this unit type
        rel_value = value / incr_settings['start']
        # get the value relative to the start of the list

        if rel_value != 0:
            index = math.floor(math.log(rel_value, int(incr_settings['factor'])))
        else:
            index = math.floor(math.log(1, int(incr_settings['factor']))) # 0 has same postfix as 1
        # calculate the index that the corresponding string is stored

        if index < 0 or index > len(incr_settings['values']):
            return str(value)

        value_representation = rel_value / math.pow(int(incr_settings['factor']), index)
        value_symbol, value_symbol_extended = list(incr_settings['values'])[index]

        return "{value} {factor}{seperator}{type}".format(
            value=type(value)(value_representation),
            factor=value_symbol if shortened else value_symbol_extended,
            seperator=incr_settings['seperator'],
            type=self.type_short if shortened else self.type_long
        )

    def clean(self):
        """
        Make sure that there is no counting type selected when the value type is not countable
        """
        super().clean()
        if (self.value_type in [short
                                for short, enum in conf_labels.VALUE_TYPES.items()
                                if enum['countable'] is False] and
                self.incremental_type):
            # string type etc.
            raise ValidationError('When the type of the unit is not countable, '
                                  'you cannot have an incremental_type specified')

    class Meta:
        ordering = ['type_short', 'type_long']
        unique_together = (
            ('type_short', 'value_type'),
            ('type_long', 'value_type')
        )
