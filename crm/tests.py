from unittest import skip

from django.test import TestCase

from crm.exceptions import CyclicParenthoodError
from crm.models import Organisation, Customer, Person, ContactOrganisation


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
    @skip("Test can't run with teardown turned on. "
          "This error is caused by a database-level failure, so can't be avoided.")
    def testInheritance(self):
        # Create a suborganisation
        beheer = Organisation.objects.create(
            name="Systeembeheer",
            email="beheer@iapc.utwente.nl",
            parent_organisation=self.iapc
        )

        schaduwbeheer = Organisation.objects.create(
            name="Schaduwsysteembeheer",
            email="schaduwbeheer@iapc.utwente.nl",
            parent_organisation=beheer
        )

        # Test if the values of beheer and schaduwbeheer are the same as those of IAPC
        for attr in ['address', 'zip_code', 'city', 'phone', 'kvk']:
            self.assertEqual(getattr(self.iapc, attr), getattr(beheer, attr),
                             "IAPC's attribute {} is different from beheer's!".format(attr))

            self.assertEqual(getattr(self.iapc, attr), getattr(schaduwbeheer, attr),
                             "IAPC's attribute {} is different from schaduwbeheer's!".format(attr))


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


class BareCustomerCreationTest(TestCase):
    """
    Tests if a bare customer (without Person or ContactOrganisation) cannot be created.
    """

    def testBareCustomer(self):
        # Try to create a bare customer
        with self.assertRaises(AttributeError):
            Customer.objects.create()

    def testPersonCustomer(self):
        Person.objects.create(
            name="Kevin Alberts",
            email="kevin@iapc.utwente.nl"
        )

        # Assert if the customer is saved
        self.assertEqual(len(Customer.objects.all()), 1)

    def testContactOrganisationCustomer(self):
        # Create person for the ContactOrganisation
        p = Person.objects.create(
            name="Kevin Alberts",
            email="kevin@iapc.utwente.nl"
        )

        # Create organisation for the ContactOrganisation
        o = Organisation.objects.create(
            name="Kevin's Organisation",
            email="organisation@kevinalberts.nl"
        )

        # Create the ContactOrganisation
        ContactOrganisation.objects.create(
            contact=p,
            organisation=o
        )

        # Check if there are now 2 customers, the Person, and the ContactOrganisation
        self.assertEqual(len(Customer.objects.all()), 2)
