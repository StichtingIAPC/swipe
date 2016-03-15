"""
This module contains the options that assortment.models uses as the basis of it's AssortmentUnitType parsing.
"""


from decimal import Decimal

import re
from django.utils.translation import ugettext as _


"""
format: {
    '<symbol of type>': {
        'as_choice': ('<symbol of type>', '<type>'),
        'parser': lambda <v>: return v parsed to this corresponding type, or raise ValueError.
        'countable': can this type be counted by increment?
    }
}

raising an error inside a lambda is not easily done, but doable by using (x for x in ()).throw(Exception)
"""
VALUE_TYPES = {
    's': {
        'as_choice': ('s', 'string'),
        'parser': lambda v: str(v)
        if re.match(r'^.+$', v)
        else (__ for __ in ()).throw(AssertionError(_('input string has to be a non-empty string'))),
        'countable': False,
    },
    'n': {
        'as_choice': ('n', 'decimal'),
        'parser': lambda v: Decimal(v)
        if re.match(r'^[0-9]+(?:\.[0-9]*)?$', v)
        else (__ for __ in ()).throw(AssertionError(_('input string has to be a non-empty string, containing at'
                                                      ' least 1 digit (0-9), and using a dot as a decimal point'))),
        'countable': True,
    },
    'i': {
        'as_choice': ('i', 'integer'),
        'parser': lambda v: int(v)
        if re.match(r'^[0-9]+$', v)
        else (__ for __ in ()).throw(AssertionError(_('input string has to be a non-empty string of at least 1 '
                                                      'digit'))),
        'countable': True,
    },
    'b': {
        'as_choice': ('b', 'boolean'),
        'parser': lambda v: bool(re.match(r'(?:[jty])|ja|true|yes', v))
        if re.match(r'^(?:[jntfy]|ja|nee|true|false|yes|no)$', v)
        else (__ for __ in ()).throw(AssertionError(_('input string has to be a non-empty string which contains'
                                                      ' a true/false value matching "[jntfy]|ja|nee|true|false|'
                                                      'yes|no"'))),
        'countable': False,
    }
}


"""
format: {
    '<symbol>': {
        'as_choice': ('<symbol>', '<explanation of the counting type>'),
        'seperator': '<character(s) to put between the multiplier and the unit type,
                            like million[ ]yen, or kilo[ ]gram>',
        'factor': <factor of increment'>,
        'start': <at what value to start the list>,
        'values': [
            ('<short notation>', '<long notation>')
        ]
    }
}
:type: dict
"""
COUNTING_TYPES = {
    'SI': {
        'as_choice': ('SI', _('the SI standard is in powers of 1000, starting with 1000^-4: f, n, u, m, [], K, ...')),
        'seperator': '',
        'factor': 1e3,
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
    },
    'ISQ': {
        'as_choice': ('ISQ', _('the ISQ standard is in powers of 1024 (2^10), starting with 1024^0: [], Ki, Mi, ...')),
        'seperator': '',
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
    },
    'EU': {
        'as_choice': ('EU', _('the EU thousands, millions and milliards `standard`')),
        'seperator': ' ',
        'factor': 1000,
        'start': 1000,
        'values': [
            ('1e3', _('thousand')),
            ('1e6', _('million')),
            ('1e9', _('milliard')),
            ('1e12', _('billion')),
            ('1e15', _('billiard')),
            ('1e18', _('trillion')),
        ],
    },
    'US': {
        'as_choice': ('US', _('the US thousands, millions and billions `standard`')),
        'seperator': ' ',
        'factor': 1000,
        'start': 1000,
        'values': [
            ('1e3', _('thousand')),
            ('1e6', _('million')),
            ('1e9', _('trillion')),
            ('1e12', _('quadrillion')),
            ('1e15', _('quintillion')),
            ('1e18', _('sextillion')),
        ],
    }
}
