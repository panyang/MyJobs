from django.test import TestCase
from django.test.client import Client
from django.core import mail
from sendgrid import SmtpApiHeader, send_mail_with_headers
from django.conf import settings
from django.template import RequestContext
from django.core.handlers.wsgi import WSGIRequest

settings.TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'app.context_processors.current_site_info'
    )


class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.

    Usage:

    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})

    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client

    Once you have a request object you can pass it to any view function,
    just as if that view had been hooked up using a URLconf.

    """
    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)


class SmtpApiTest(TestCase):
    """Test suite for SendGrid smpt header object"""

    def test_smtpaipheader_addCategory(self):
        """Test SendGrid SMTP Header with just a category."""
        h = SmtpApiHeader()
        h.setCategory("Transactional")
        # we are testing a string against a string
        self.assertEqual(h.__str__(),
                         'X-SMTPAPI: {"category": "Transactional"}')

    def test_smtpapiheader_addTo(self):
        """Test SendGrid SMTP header with recipients"""
        expected = 'X-SMTPAPI: {"to": ["kyle@somewhere.com", ' + \
            '"bob@someplace.net", "someguy@googlemailz.coms"]}'
        tos = ['kyle@somewhere.com',
               'bob@someplace.net',
               'someguy@googlemailz.coms']
        h = SmtpApiHeader()
        h.addTo(tos)
        # remember we are testing a string against a string
        self.assertEqual(h.__str__(), expected)

    def test_smtpapiheader_setUniqueArgs(self):
        """Test SendGrid SMTP Header unique args"""
        expected = 'X-SMTPAPI: {"unique_args": {"testa": 1, "testb": 2}}'
        h = SmtpApiHeader()
        h.setUniqueArgs({'testa': 1, 'testb': 2})
        self.assertEqual(h.__str__(), expected)

    def test_smtpapiheader_asJSON(self):
        """Test SendGrid SMTP headers work as JSON"""
        expected = '{"category": "Transactional"}'
        h = SmtpApiHeader()
        h.setCategory("Transactional")
        # yes, it says asJSON, but it's a string of JSON not a JSON object
        self.assertEqual(h.asJSON(), expected)

    def test_smtpapiheader_as_django_header(self):
        """Test django ready email header dict."""
        expected = {'X-SMTPAPI': '{"category": "foo", "filters": {"category": {"settings": {"setting": "value"}}}}'}
        h = SmtpApiHeader()
        h.setCategory('foo')
        h.addFilterSetting('category', 'setting', 'value')
        self.assertEqual(h.as_django_email_header(), expected)
        
    def test_send_mail_with_headers(self):
        """Test SendGrid send_mail wrapper"""

        # Use Django's memeory backend to test sending
        subject = "Test Message"
        from_email = "test@somewhare.com"
        recipient_list = ['somedude@someplace', 'otherduded@otherplace.com']
        message = "ABC123"
        backend = 'django.core.mail.backends.locmem.EmailBackend'
        # clear out outbox
        mail.outbox = []
        connection = mail.get_connection(backend=backend)
        # Make the email
        send_mail_with_headers(subject, message, from_email,
                               recipient_list, connection=connection)
        self.assertEqual(len(mail.outbox), 1)
        # make sure that API headers are present
        self.assertTrue(mail.outbox[0].message().__str__().\
                        find('transactional'))


class ContextProcessorTest(TestCase):
    """Test suite for context processors."""

    def test_current_site_info(self):
        """Test current_site_info context is actually adding to context"""
        rf = RequestFactory()
        get_request = rf.get('/')
        context = RequestContext(get_request)
        self.assertEqual(context['site_name'], 'example.com')
        self.assertEqual(context['site_domain'], 'example.com')
