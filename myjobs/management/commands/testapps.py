from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from default_settings import PROJECT_APPS

class Command(BaseCommand):
    help = 'Runs all project app tests'

    def handle(self, *args, **options):
        for app in PROJECT_APPS:
            self.stdout.write('Testing app: %s' % app)
            call_command('test', app)
            self.stdout.write('\n')
