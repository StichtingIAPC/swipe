from django.core.management.base import BaseCommand, CommandError
from register.models import ConsistencyChecker
from stock.models import Stock


#TODO : Decide on formal format for errors, and write all tests in that format
checkers = [ConsistencyChecker.full_check, Stock.do_check]
class Command(BaseCommand):

    def handle(self, *args, **options):
        for checker in checkers:
            checker()
