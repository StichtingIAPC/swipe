from django.core.management.base import BaseCommand, CommandError
from register.models import ConsistencyChecker


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Starting consistency check")
        ConsistencyChecker.full_check()
        print("Check completed, no errors found")