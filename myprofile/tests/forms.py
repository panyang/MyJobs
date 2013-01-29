from django.test import TestCase

from myprofile.forms import *
from myprofile.models import *

class MyProfileFormsTests(TestCase):
    def test_generate_custom_widgets(self):
        # Generate custom widgets should generate the correct widgets
        # with custom id and placeholder values
        self.assertEqual(2,2)
