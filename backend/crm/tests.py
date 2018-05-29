from django.contrib.auth.models import User
from django.test import TestCase

from crm.exceptions import CyclicParenthoodError
from crm.models import Organisation, Customer, Person, ContactOrganisation, SwipePermission, SwipePermissionGroup


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


class PermissionTests(TestCase):

    def setUp(self):
        self.p1 = SwipePermission(name="Test1")
        self.p2 = SwipePermission(name="Test2")
        self.p3 = SwipePermission(name="Test3")
        self.p4 = SwipePermission(name="Test4")
        self.p1.save()
        self.p2.save()
        self.p3.save()
        self.p4.save()
        self.g1 = SwipePermissionGroup(name="Group1")
        self.g2 = SwipePermissionGroup(name="Group2")
        self.g1.save()
        self.g2.save()
        self.user1 = User(username="Testname")
        self.user1.save()

    def testConnection(self):
        self.p1.groups.add(self.g1)
        self.p1.groups.add(self.g2)
        self.p2.groups.add(self.g1)
        self.p3.groups.add(self.g2)
        self.g1.users.add(self.user1)
        self.assertEqual(SwipePermission.objects.filter(groups__name="Group2").count(), 2)
        self.assertTrue(SwipePermission.objects.filter(groups__users=self.user1).exists())
        self.assertTrue(SwipePermission.objects.filter(name="Test1", groups__users=self.user1).exists())
        self.assertFalse(SwipePermission.objects.filter(name="Test3", groups__users=self.user1).exists())
        self.assertTrue(SwipePermission.user_has_permission(self.user1, "Test1"))
        self.assertFalse(SwipePermission.user_has_permission(self.user1, "Test3"))

