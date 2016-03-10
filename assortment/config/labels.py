from decimal import Decimal

import re
from django.utils.translation import ugettext as _


ENUMERATION_TYPES = (
    ('s', _('string')),
    ('n', _('decimal')),
    ('i', _('integer')),
    ('b', _('boolean')),
)


NON_COUNTABLE_ENUMERATION_TYPES = ('s', 'b')


ENUMERATION_PARSERS = {
    's': lambda v:
        str(v) if re.match(
            r'^.+$', v)
        else (_ for _ in ()).throw(AssertionError(_('input string has to be a non-empty string'))),
    'n': lambda v:
        Decimal(v) if re.match(
            r'^[0-9]+(?:\.[0-9]*)?$', v)
        else (_ for _ in ()).throw(AssertionError(_('input string has to be a non-empty string, containing at least 1 '
                                                  'digit (0-9), and using a dot as a decimal point'))),
    'i': lambda v:
        int(v) if re.match(
            r'^[0-9]+$', v)
        else (_ for _ in ()).throw(AssertionError(_('input string has to be a non-empty string of at least 1 digit'))),
    'b': lambda v:
        bool(re.match(r'(?:[jty])|ja|true|yes', v)) if re.match(
            r'^(?:[jntfy]|ja|nee|true|false|yes|no)$', v)
        else (_ for _ in ()).throw(AssertionError(_('input string has to be a non-empty string which contains a '
                                                  'true/false value matching "[jntfy]|ja|nee|true|false|yes|no"'))),
}

# format: tuple<tuple<str1, str1>>. len(str1) is max 3 (see UnitType.incremental_type
SYMBOL_TYPES = (
    ('SI', _('the SI standard is in powers of 1000, starting with 1000^-4: f, n, u, m, [], K, M, G, T, P, E, ...')),
    ('ISQ', _('the ISQ standard is in powers of 1024 (2^10), starting with 1024^0: [], Ki, Mi, Gi, Ti, Pi, Ei, ...')),
    ('EU', _('the EU thousands, millions and milliards `standard`')),
    ('US', _('the US thousands, millions and billions `standard`')),
)


SYMBOL_EXTENDED = {
    'SI': {
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
        'seperator': '',
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
        'seperator': '',
    },
    'EU': {
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
        'seperator': ' ',
    },
    'US': {
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
        'seperator': ' ',
    }
}
