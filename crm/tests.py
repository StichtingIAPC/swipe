from django.test import TestCase

from crm.exceptions import CyclicParenthoodError
from crm.models import Organisation


class OrganisationInheritanceTest(TestCase):
    """
    Tests the inheritance of organisations.
    """

    def setUp(self):
        # Create a base organisation
        self.iapc = Organisation.objects.create(
            name="Stichting IAPC",
            email="bestuur@iapc.utwente.nl",
            address="Drienerlolaan 5",
            zip_code="7522 ND",
            city="Enschede",
            phone="053-4893927",
            kvk="41029973",
            memo="Super ruige Stichting"
        )

    def testInheritance(self):
        # Create a suborganisation
        beheer = Organisation.objects.create(
            name="Systeembeheer",
            email="beheer@iapc.utwente.nl",
            parent_organisation=self.iapc
        )

        # Test if the values of beheer are the same as those of IAPC
        for attr in ['address', 'zip_code', 'city', 'phone', 'kvk']:
            self.assertEqual(getattr(self.iapc, attr), getattr(beheer, attr),
                             "IAPC's attribute {} is different from beheer's!".format(attr))


class OrganisationCycleDetectionTest(TestCase):
    """
    Tests if the cycle detection works in organisations.
    """

    def setUp(self):
        # Create a base organisation
        self.iapc = Organisation.objects.create(
            name="Stichting IAPC",
            email="bestuur@iapc.utwente.nl",
            address="Drienerlolaan 5",
            zip_code="7522 ND",
            city="Enschede",
            phone="053-4893927",
            kvk="41029973",
            memo="Super ruige Stichting"
        )

        # Create a suborganisation
        self.beheer = Organisation.objects.create(
            name="Systeembeheer",
            email="beheer@iapc.utwente.nl",
            parent_organisation=self.iapc
        )

        # Create another suborganisation
        self.schaduwbeheer = Organisation.objects.create(
            name="Schaduwsysteembeheer",
            email="schaduwbeheer@iapc.utwente.nl",
            parent_organisation=self.beheer
        )

    def testNoCycles(self):
        # Test if the default setup indeed does not contain loops.
        self.assertFalse(self.schaduwbeheer._has_cycle(), "The default setup for the loop test has a loop!")

    def testCycles(self):
        # Change IAPC's parent to schaduwbeheer.
        self.iapc.parent_organisation = self.schaduwbeheer

        # Check if the cycle detection now detects a cycle
        self.assertTrue(self.iapc._has_cycle())

        # Try to save the object, which should raise an error.
        with self.assertRaises(CyclicParenthoodError):
            self.iapc.save()

