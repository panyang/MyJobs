from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

from myjobs.models import User
from myjobs.tests.factories import UserFactory
from myprofile.tests.factories import PrimaryNameFactory


class CommonTagsTests(TestCase):
    def setUp(self):
        super(CommonTagsTests, self).setUp()
        self.user = UserFactory()
        self.context = Context({'user': self.user})

    def test_get_name_obj_no_name(self):
        template = Template(
                    '{% load common_tags %}'
                    '{{ user|get_name_obj }}'
                 )
        out = template.render(self.context)
        self.assertEqual(out, '')

    def test_get_name_obj_with_name(self):
        template = Template(
                    '{% load common_tags %}'
                    '{{ user|get_name_obj }}'
                 )
        name = PrimaryNameFactory(user=self.user)
        out = template.render(self.context)
        self.assertEqual(out, name.get_full_name())

    def test_get_name_obj_with_default(self):
        template = Template(
                    '{% load common_tags %}'
                    '{{ user|get_name_obj:"Default value" }}'
                 )
        out = template.render(self.context)
        self.assertEqual(out, 'Default value')
