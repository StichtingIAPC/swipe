from django.core.management.base import BaseCommand, CommandError
from register.models import ConsistencyChecker
from stock.models import Stock


# Temporary formal format for errors: text: text description of error, location: part of program that has the error, line: reference to where the error can be found
checkers = {"cashregister": ConsistencyChecker.non_crashing_full_check, "stock": Stock.do_check}


class Command(BaseCommand):
    def handle(self, *args, **options):
        errors = False
        for checker in checkers.keys():
            result = checkers[checker]()
            if result:
                if not errors:
                    errors=True
                    print("Errors found:")
                    print("TEST        | Location |    Line    | Texts")
                    print("-------------------------------------------")
                for res in result:
                    print("{:12s}|{:10s}|{:12s}|{}".format(checker[0:12], res["location"].__str__()[0:10],res["line"].__str__()[0:12],res["text"]))
        if not errors:
            print("No errors found")