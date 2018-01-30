from django.test import TestCase

from crm.models import Person
from tools.testing import TestData

# Create your tests here.
class DeletionTest(TestCase, TestData):

    def setUp(self):
        pass

    def test_delete_active_person(self):
        person = Person(name="Jan", email="email")
        person.save()
        db_person = Person.objects.get(name="Jan")
        self.assertFalse(db_person.is_deleted)
        person.delete()
        db_person_updated = Person.objects.all_with_deleted().get(name="Jan", is_deleted=True)
        self.assertTrue(db_person_updated.is_deleted)