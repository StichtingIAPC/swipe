from django.core.management.base import BaseCommand

# Temporary formal format for errors: text: text description of error,
# location: part of program that has the error, line: reference to where the error can be found
from mockdatagen.models import execute, do_in_order
# noinspection PyUnresolvedReferences : Used to import classes by force.
from mockdatagen.mocks import money, register, article, customer
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        User.objects.create_superuser("swipe", 'swipe@iapc.utwente.nl', 'swipersdoswipe')
        print(User.objects.all())
        do_in_order(execute)
