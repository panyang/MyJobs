from bs4 import BeautifulSoup

from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

from myjobs.forms import EditAccountForm
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

class FormTagsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.form = EditAccountForm(user=self.user, data={})
        self.context = Context({'form': self.form})
        self.template = Template(
                         '{% load form_tags %}'
                         '{% add_required_label form.visible_fields.2 %}'
                      )

    def test_add_required_label(self):
        self.form.data['gravatar'] = self.user.email
        out = self.template.render(self.context)
        soup = BeautifulSoup(out)
        self.assertEqual(soup.label['class'], [u''])

    def test_add_required_label_bad_form(self):
        out = self.template.render(self.context)
        soup = BeautifulSoup(out)
        self.assertEqual(soup.label['class'], [u'label-required'])

    def test_add_required_label_extra_classes(self):
        self.template = Template(
                         '{% load form_tags %}'
                         '{% add_required_label form.visible_fields.2 "extra-class" %}'
                      )
        out = self.template.render(self.context)
        soup = BeautifulSoup(out)
        self.assertItemsEqual(soup.label['class'], [u'extra-class', u'label-required'])
