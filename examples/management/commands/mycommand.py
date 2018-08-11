from demosys.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test command"

    def add_arguments(self, parser):
        parser.add_argument("message", help="A message")

    def handle(self, *args, **options):
        print("The message was:", options['message'])
