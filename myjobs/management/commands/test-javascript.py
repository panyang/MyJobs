import webbrowser
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs all project app tests'

    def handle(self, *args, **options):
        # open a browser to run qUnit javascript tests
        print "opening tests in default browser"
        test_browser = webbrowser.open("templates/tests/def.ui.tests.html")
        if test_browser:
            print "Review tests & close when when complete (or type 'Ctrl+C')"
        else:
            print "There was an error: %s" % test_browser
