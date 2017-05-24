from django.core.management.base import BaseCommand

# Temporary formal format for errors: text: text description of error,
# location: part of program that has the error, line: reference to where the error can be found
from mockdatagen.models import execute, do_in_order
from mockdatagen.mocks import money


class Command(BaseCommand):
    def handle(self, *args, **options):
        do_in_order(execute)
