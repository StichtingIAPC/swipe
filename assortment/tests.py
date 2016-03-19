from unittest import skip

from django.test import TestCase
from django.utils.translation import ugettext as _

from assortment.models import *
from assortment.config.labels import *


class BasicTest(TestCase):
    def setUp(self):
        self.make_unit_types()
        self.make_label_types()
        self.make_labels()

    def make_unit_types(self):
        self.stringType = AssortmentUnitType.objects.create(
            type_short='',          # strings do not have a measurable dimension
            type_long='',           # description
            counting_type='s'       # s for string
        )
        self.countableIntTypeHertz = AssortmentUnitType.objects.create(
            type_short='Hz',        # Hz is just an example of integer values.
            type_long='hertz',       #
            counting_type='i',      # i for integer
            incremental_type='SI'   # SI counting for this unittype
        )
        self.numberTypeMeter = AssortmentUnitType.objects.create(
            type_short='m',         # meter
            type_long='meter',      #
            counting_type='n'       # n for number
        )
        self.booleanType = AssortmentUnitType.objects.create(
            type_short='',          # booleans do not have any long/short type either
            type_long='',           # as you might expect: it would not make sense
            counting_type='b'       # b for boolean
        )
        self.normalInt = AssortmentUnitType.objects.create(
            type_short='s',
            type_long='seconds',
            counting_type='i'
        )

    def make_label_types(self):
        self.labelType = AssortmentLabelType.objects.create(
            description='Cable length',
            name='length',
            unit_type=self.numberTypeMeter
        )
        self.countableLabelType = AssortmentLabelType.objects.create(
            description='CPU cycles per second',
            name='cpu speed',
            unit_type=self.countableIntTypeHertz
        )
        self.non_countableLabelType = AssortmentLabelType.objects.create(
            description='GPU brand label',
            name='brand',
            unit_type=self.stringType
        )

    def make_labels(self):
        self.cable_five_meters = self.labelType.label(5)
        self.cable_four_meters = self.labelType.label(4)
        self.cpu_five_khz = self.countableLabelType.label(5000)
        self.cpu_fifteen_khz = self.countableLabelType.label(15000)

    def validation_error_unit_type_create(self, **kwargs):
        try:
            AssortmentUnitType.objects.create(**kwargs)
        except Exception as e:
            raise ValidationError(str(e))

    def test_create_unit_type(self):
        assert (self.stringType and
                self.countableIntTypeHertz and
                self.numberTypeMeter and
                self.booleanType and
                self.normalInt)
        self.assertRaises(ValidationError, self.validation_error_unit_type_create,
                          type_short='',
                          type_long='',
                          counting_type='s'
                          )  # fail to create a duplicate UnitType
        self.assertRaises(ValidationError, self.validation_error_unit_type_create,
                          type_short='s',
                          type_long='seconds',
                          counting_type='b',
                          incremental_type='SI'
                          )  # fail to create an UnitType which has an incremental type, but cannot be counted

    def test_unit_type_conversion(self):
        string = 'string'
        integer = '123'
        decimal = '1.2'
        boolean = 'true'

        assert isinstance(self.stringType.parse(string), str)
        assert isinstance(self.stringType.parse(integer), str)
        assert isinstance(self.stringType.parse(decimal), str)
        assert isinstance(self.stringType.parse(boolean), str)

        self.assertRaises(AssertionError, self.countableIntTypeHertz.parse, string)
        assert isinstance(self.countableIntTypeHertz.parse(integer), int)
        self.assertRaises(AssertionError, self.countableIntTypeHertz.parse, decimal)
        self.assertRaises(AssertionError, self.countableIntTypeHertz.parse, boolean)

        self.assertRaises(AssertionError, self.numberTypeMeter.parse, string)
        assert isinstance(self.numberTypeMeter.parse(integer), Decimal)
        assert isinstance(self.numberTypeMeter.parse(decimal), Decimal)
        self.assertRaises(AssertionError, self.numberTypeMeter.parse, boolean)

        self.assertRaises(AssertionError, self.booleanType.parse, string)
        self.assertRaises(AssertionError, self.booleanType.parse, integer)
        self.assertRaises(AssertionError, self.booleanType.parse, decimal)
        assert isinstance(self.booleanType.parse(boolean), bool)

    def test_clean_unit_type(self):
        test = AssortmentUnitType(type_short='', type_long='', counting_type='b', incremental_type='SI')
        self.assertRaises(ValidationError, test.clean)

    def test_label_type_creation(self):
        assert (self.labelType and self.countableLabelType)

    def test_label_creation(self):
        assert (self.cable_five_meters and
                self.cable_four_meters and
                self.cpu_five_khz and
                self.cpu_fifteen_khz)
        self.assertEqual(self.cable_five_meters, self.labelType.label('5'))
        self.assertRaises(AssertionError, AssortmentLabel.get, value=6, label_type=self.labelType)
        self.assertRaises(AssertionError, self.make_label, value='5', label_type=self.labelType)

    def make_label(self, value, label_type):
        try:
            AssortmentLabel.objects.create(value=value, label_type=label_type)
            AssortmentLabel.objects.create(value=value, label_type=label_type)
        except Exception as e:
            raise AssertionError(str(e))

    def test_get_label(self):
        self.assertEqual(AssortmentLabel.get('5', self.countableLabelType),
                         AssortmentLabel.get('5', self.countableLabelType))
        self.assertEqual(AssortmentLabel.get('1.2', self.labelType),
                         AssortmentLabel.get('1.20', self.labelType))
        self.assertEqual(self.labelType.label('1.2'),
                         self.labelType.label('1.20'))
