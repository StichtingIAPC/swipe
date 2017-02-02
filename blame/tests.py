from time import sleep

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from blame.models import ImmutableBlameTest, BlameTest, BlameLog, \
    ImmutableBlameEditException


class OrderTest(TestCase):
    def test_immutable(self):
        u = User.objects.create()
        ib = ImmutableBlameTest.objects.create(data=1, user_created=u)
        ib.data = 2

        self.assertEqual(len(BlameLog.objects.all()), 1)
        self.assertEqual(ib.user_created, u)

        with self.assertRaises(ImmutableBlameEditException):
            ib.save()

    def test_create_update(self):
        u = User.objects.create(username="HARRY")
        ib = BlameTest.objects.create(data=1, user_modified=u)
        u = User.objects.create(username="AAAAAA")
        sleep(0.01)  # Force date_modified to change

        ib.user_modified = u
        ib.data = 2
        ib.save()

        self.assertNotEqual(ib.user_created, ib.user_modified)
        self.assertNotEqual(ib.date_created, ib.date_modified)
        self.assertEqual(len(BlameLog.objects.all()), 2)
