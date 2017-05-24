from django.core.management.base import BaseCommand

# Temporary formal format for errors: text: text description of error,
# location: part of program that has the error, line: reference to where the error can be found
from mockdatagen.models import execute, do_in_order

CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"
checkers = []


def consistency_check(func):
    checkers.append(func)
    return func


class Command(BaseCommand):
    def handle(self, *args, **options):
        do_in_order(execute)
