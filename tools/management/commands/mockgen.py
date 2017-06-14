from django.core.management.base import BaseCommand

# Temporary formal format for errors: text: text description of error,
# location: part of program that has the error, line: reference to where the error can be found
from mockdatagen.helpers import MockGen

# noinspection PyUnresolvedReferences : Used to import classes by force.
from mockdatagen.mocks import money, register, article, customer
from django.contrib.auth.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--yes-i-am-sure',
            action='store_true',
            dest='ok',
            default=False,
            help='Actually run the command.'
        )

    def handle(self, *args, ok, **options):
        # Check for --yes-i-am-sure flag
        if not ok:
            self.stdout.write("To actually run the command, use the option '--yes-i-am-sure'. ")
            return
        User.objects.all().delete()
        User.objects.create_superuser("swipe", 'swipe@iapc.utwente.nl', 'swipersdoswipe')
        print(User.objects.all())
        mg_inst = MockGen.get_instance()
        mg_inst.do_in_order(mg_inst.execute)
