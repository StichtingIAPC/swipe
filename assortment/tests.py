from django.db import transaction, IntegrityError
from django.test import TestCase

from assortment.config.labels import *
from assortment.models import *
from tools.util import _assert


class BasicTest(TestCase):
    def setUp(self):
        self.make_unit_types()
        self.make_label_types()
        self.make_labels()

    def make_unit_types(self):
        self.stringType = AssortmentUnitType.objects.create(
            type_short='',          # strings do not have a measurable dimension
            type_long='',           # description
            value_type='s'          # s for string
        )
        self.countableIntTypeHertz = AssortmentUnitType.objects.create(
            type_short='Hz',        # Hz is just an example of integer values.
            type_long='hertz',      #
            value_type='i',         # i for integer
            incremental_type='SI'   # SI counting for this unittype
        )
        self.numberTypeMeter = AssortmentUnitType.objects.create(
            type_short='m',         # meter
            type_long='meter',      #
            value_type='n'          # n for number
        )
        self.booleanType = AssortmentUnitType.objects.create(
            type_short='',          # booleans do not have any long/short type either
            type_long='',           # as you might expect: it would not make sense
            value_type='b'          # b for boolean
        )
        self.normalInt = AssortmentUnitType.objects.create(
            type_short='s',
            type_long='seconds',
            value_type='i'
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

    def test_create_unit_type(self):
        _assert(self.stringType and
                self.countableIntTypeHertz and
                self.numberTypeMeter and
                self.booleanType and
                self.normalInt)
        with transaction.atomic():
            self.assertRaises(IntegrityError, AssortmentUnitType.objects.create,
                              type_short='',
                              type_long='',
                              value_type='s'
                              )  # fail to create a duplicate UnitType
        with transaction.atomic():
            self.assertRaises(ValidationError, AssortmentUnitType.objects.create,
                              type_short='s',
                              type_long='seconds',
                              value_type='b',
                              incremental_type='SI'
                              )  # fail to create an UnitType which has an incremental type, but cannot be counted

    def test_unit_type_conversion(self):
        string = 'string'
        integer = '123'
        decimal = '1.2'
        boolean = 'true'

        _assert(isinstance(self.stringType.parse(string), str))
        _assert(isinstance(self.stringType.parse(integer), str))
        _assert(isinstance(self.stringType.parse(decimal), str))
        _assert(isinstance(self.stringType.parse(boolean), str))

        self.assertRaises(AssertionError, self.countableIntTypeHertz.parse, string)
        _assert(isinstance(self.countableIntTypeHertz.parse(integer), int))
        self.assertRaises(AssertionError, self.countableIntTypeHertz.parse, decimal)
        self.assertRaises(AssertionError, self.countableIntTypeHertz.parse, boolean)

        self.assertRaises(AssertionError, self.numberTypeMeter.parse, string)
        _assert( isinstance(self.numberTypeMeter.parse(integer), Decimal))
        _assert( isinstance(self.numberTypeMeter.parse(decimal), Decimal))
        self.assertRaises(AssertionError, self.numberTypeMeter.parse, boolean)

        self.assertRaises(AssertionError, self.booleanType.parse, string)
        self.assertRaises(AssertionError, self.booleanType.parse, integer)
        self.assertRaises(AssertionError, self.booleanType.parse, decimal)
        _assert( isinstance(self.booleanType.parse(boolean), bool))

    def test_clean_unit_type(self):
        test = AssortmentUnitType(type_short='', type_long='', value_type='b')
        test.incremental_type = 'SI'
        self.assertRaises(ValidationError, test.clean)

    def test_label_type_creation(self):
        _assert(self.labelType and self.countableLabelType)

    def test_label_creation(self):
        _assert(self.cable_five_meters and
                self.cable_four_meters and
                self.cpu_five_khz and
                self.cpu_fifteen_khz)
        self.assertEqual(self.cable_five_meters, self.labelType.label('5'))
        self.assertRaises(AssertionError, AssortmentLabel.get, value=6, label_type=self.labelType)
        self.assertRaises(IntegrityError, self.make_label, value='5', label_type=self.labelType)

    def make_label(self, value, label_type):
        AssortmentLabel.objects.create(value=value, label_type=label_type)
        AssortmentLabel.objects.create(value=value, label_type=label_type)

    def test_get_label(self):
        self.assertEqual(AssortmentLabel.get('5', self.countableLabelType),
                         AssortmentLabel.get('5', self.countableLabelType))
        self.assertEqual(AssortmentLabel.get('1.2', self.labelType),
                         AssortmentLabel.get('1.20', self.labelType))
        self.assertEqual(self.labelType.label('1.2'),
                         self.labelType.label('1.20'))


class BranchTests(TestCase):
    def setUp(self):
        self.assortment_branches = list()
        a = self.assortment_branches
        a.append(AssortmentArticleBranch(name="root", parent_tag=None))
        a.append(AssortmentArticleBranch(name="cables", parent_tag=a[0]))
        a.append(AssortmentArticleBranch(name="root2", parent_tag=None))
        a.append(AssortmentArticleBranch(name="cycle", parent_tag=None))
        a[3].parent_tag = a[3]

    def test_branch_creation(self):
        self.assortment_branches[0].save()
        self.assortment_branches[1].save()

    def test_branch_cycles(self):
        self.assertRaises(ValidationError, self.assortment_branches[3].save)

    def test_branch_double_root(self):
        self.assortment_branches[0].save()
        self.assertRaises(ValidationError, self.assortment_branches[2].save)
