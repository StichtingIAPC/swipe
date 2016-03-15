from django.core.management.base import BaseCommand, CommandError


# Temporary formal format for errors: text: text description of error, location: part of program that has the error, line: reference to where the error can be found

checkerz = []
def consistency_check(func):
    checkerz.append(func)
    return func

class Command(BaseCommand):
    def handle(self, *args, **options):
        errors = False
        for checker in checkerz:
            result = checker()
            print (checker.__name__)
            if result:
                if not errors:
                    errors=True
                    print("Errors found:")
                    print("SEVERITY|TEST        | Location |    Line    | Texts")
                    print("-------------------------------------------")
                for res in result:
                    print("{:8s}|{:10s}|{:12s}|{}".format(res.pop("severity","")[0:8], res["location"].__str__()[0:10],res["line"].__str__()[0:12],res["text"]))
        if not errors:
            print("No errors found")