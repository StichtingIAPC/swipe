import re

from decimal import Decimal
from django.db import models


COUNTING_TYPES = (
    ('s', 'string'),
    ('n', 'decimal'),
    ('i', 'integer'),
    ('b', 'boolean'),
)

COUNTING_PARSERS = {
    's': lambda v: str(v) if re.match(
        r'^.+$', v) else (_ for _ in ()).throw(
        AssertionError('input string has to be a non-empty string')),
    'n': lambda v: Decimal(v) if re.match(
        r'^[0-9]+(?:\.[0-9]*)?$', v) else (_ for _ in ()).throw(
        AssertionError('input string has to be a non-empty string, containing at least 1 digit (0-9), '
                       'and using a dot as a decimal point')),
    'i': lambda v: int(v) if re.match(
        r'^[0-9]+$', v) else (_ for _ in ()).throw(
        AssertionError('input string has to be a non-empty string of at least 1 digit (0-9)')),
    'b': lambda v: bool(re.match(r'(?:[jty])|ja|true|yes', v)) if re.match(
        r'^(?:[jntfy]|ja|nee|true|false|yes|no)$', v) else (_ for _ in ()).throw(
        AssertionError('input string has to be a non-empty string which contains a true/false value matching "'
                       '[jntfy]|ja|nee|true|false|yes|no"')),
}

SYMBOL_TYPES = (
    ('SI', 'the SI standard is in powers of 1000, starting with 1000^-4: f, n, u, m, [], K, M, G, T, P, E, ...'),
    ('ISQ', 'the ISQ standard is in powers of 1024 (2^10), starting with 1024^0: [], Ki, Mi, Gi, Ti, Pi, Ei, ...'),
    ('EU', 'the EU millions and milliards `standard`'),
    ('US', 'the US millions and billions `standard`'),
)


SYMBOL_EXTENDED = {
    'SI': {
        'factor': 1000,
        'start': 1e-12,
        'values': [
            ('f', 'femto'),
            ('n', 'nano'),
            ('u', 'micro'),
            ('m', 'milli'),
            ('', ''),
            ('K', 'kilo'),
            ('M', 'mega'),
            ('G', 'giga'),
            ('T', 'tera'),
            ('P', 'peta'),
            ('E', 'exa')
        ],
        'seperator': ''
    },
    'ISQ': {
        'factor': 1024,
        'start': 1024,
        'values': [
            ('Ki', 'kibi'),
            ('Mi', 'mibi'),
            ('Gi', 'gibi'),
            ('Ti', 'tebi'),
            ('Pi', 'pebi'),
            ('Ei', 'exbi')
        ],
        'seperator': ''
    },
    'EU': {
        'factor': 1000,
        'start': 1000,
        'values': [
            ('1e3', 'thousand'),
            ('1e6', 'million'),
            ('1e9', 'milliard'),
            ('1e12', 'billion'),
            ('1e15', 'billiard'),
            ('1e18', 'trillion'),
        ],
        'seperator': ' '
    },
    'US': {
        'factor': 1000,
        'start': 1000,
        'values': [
            ('1e3', 'thousand'),
            ('1e6', 'million'),
            ('1e9', 'trillion'),
            ('1e12', 'quadrillion'),
            ('1e15', 'quintillion'),
            ('1e18', 'sextillion'),
        ],
        'seperator': ' '
    }
}


class Label(models.Model):
    value = models.TextField(max_length=64, editable=False)
    label_type = models.ForeignKey('LabelType', on_delete=models.CASCADE, editable=False)

    def __init__(self, value, label_type):
        if not isinstance(value, str):
            raise AssertionError('initial `value` must be of type str')

        self.label_type = label_type
        self._value = label_type.unit_type.parse(value)
        self.value = str(self._value)
        super().__init__()

    def __str__(self):
        return self.label_type.to_string(self.value)

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

    def __init__(self):
        super().__init__()

    def to_string(self, value):
        return "{}: {}{}".format(self.name_short, value, self.unit_type.type_short)

    def label(self, val):
        value = self.unit_type.parse(val)
        return Label.objects.get_or_create(value=value, label_type=self.pk)


class UnitType(models.Model):
    type_short = models.CharField(max_length=32, unique=True, editable=False)
    type_long = models.CharField(max_length=2, unique=True, editable=False)
    counting_type = models.CharField(max_length=1, choices=COUNTING_TYPES, editable=False)
    incremental_type = models.CharField(max_length=3, choices=SYMBOL_TYPES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{} seen as {} using type {}".format(self.type_long, self.type_short, self.get_counting_type_display())

    def parse(self, value):
        return COUNTING_PARSERS[self.counting_type](value)

    class Meta:
        ordering = ['type_short', 'type_long']
