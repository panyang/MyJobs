"""
sendgrid.py

Implements SendGrid's SMTP api and provdes a Django send_mail replacement 

Authors:

- SendGrid.com -- http://sendgrid.com
- Mike Seidle -- http://directemployersfoundation.org
  mike@directemployersfoundation.org
"""

import json
import re
import textwrap
from django.core import mail


class SmtpApiHeader:
    """Creates mail header for SendGrid SMTP API

    Creates folded X-SMTPAPI header for passing settings to the SendGrid
    SMTP API.

    Documentation for the SendGrid API is available at:
    http://docs.sendgrid.com/documentation/api/smtp-api/
    """

    def __init__(self):
        self.data = {}

    def addTo(self, to):
        """Adds a list of recipients

        Arguments:

        - to -- a list of email addresses
        """

        if 'to' not in self.data:
            self.data['to'] = []
        if type(to) is str:
            self.data['to'] += [to]
        else:
            self.data['to'] += to

    def addSubVal(self, var, val):
        """Adds substitution values to SendGrid header

        Substitution values are inserted into the body of the message
        where <% %> tags appear. Values must be set for each recipient
        address. Arguments:

        - var -- name of substitution tag
        - val -- list of values for the tag for each recipient.
        """

        if 'sub' not in self.data:
            self.data['sub'] = {}
        if type(val) is str:
            self.data['sub'][var] = [val]
        else:
            self.data['sub'][var] = val

    def setUniqueArgs(self, val):
        """Sets Unique Argument for all emails.

        Arguments:

        - val -- a dictionary of unique values. eg. {"batch": "200"}
        """

        if type(val) is dict:
            self.data['unique_args'] = val

    def setCategory(self, cat):
        """Adds a category to the SendGrid header
        
        Arguments:
        
        - cat -- string containing category
        """
        self.data['category'] = cat

    def addFilterSetting(self, fltr, setting, val):
        """ Adds a filter setting header. Filter = Sendgrid app setting.
        
        Arguments 
        
        - fltr -- The name of the SendGrid App
        - setting -- The SendGrid App  setting being changed
        - value -- The actual value of the setting.
        """
        
        if 'filters' not in self.data:
            self.data['filters'] = {}
        if fltr not in self.data['filters']:
            self.data['filters'][fltr] = {}
        if 'settings' not in self.data['filters'][fltr]:
                self.data['filters'][fltr]['settings'] = {}
        self.data['filters'][fltr]['settings'][setting] = val

    def asJSON(self):
        """ Returns Sendgrid API settings as JSON."""

        j = json.dumps(self.data)
        return re.compile('(["\]}])([,:])(["\[{])').sub('\1\2 \3', j)

    def as_string(self):
        """returns an X-SMTPAPI header string

        __str__ is more pythonic, this is kept for compatiblity with
        SendGrid's existing documentation.
        """

        j = self.asJSON()
        str = 'X-SMTPAPI: %s' %  j #textwrap.fill(j, subsequent_indent='  ', width=72)
        return str

    def as_django_email_header(self):
        """returns X-SMTPAPI JSON in a way Django can use"""
        
        key = "X-SMTPAPI"
        value = self.asJSON()
        return {key: value}

    def __str__(self):
        """returns sendgrid api X-SMTPAPI header as a string.

        Note: Calls as_string in case something is looking for
        __str__.
        """

        return self.as_string()

def send_mail_with_headers(subject, message, from_email, recipient_list,
                           fail_silently=False, auth_user=None,
                           auth_password=None, connection=None,
                           headers={}):
    """Allows Django to send mail via SendGrid with SendGrid SMTP API headers.
       
       If you import this as send_mail, your existing Django using 
       django.mail.send_mail with work with sendgrid. 
       
       Parameters:
       
       - subject -- Subject of message
       - message -- Actual message
       - from_email -- email address that message is from
       - recipient_list -- list of recipients ['joe@test.com','bill@test.com...]
       - fail_silently -- True or False
       - auth_user -- SMTP user. Uses ettings.py default.
       - auth_password -- Password for SMTP user. Uses settings.py default.
       - connection -- a django.mail.connection 
       - headers -- an dict containing a properly formatted sendgrid API header
                    ordinarily some_smt_papi_header.as_django_smtp_header()
       
       """

    # make sure we have a connection to send to.
    if not connection:
        connection = mail.get_connection()
    # form the message with headers.
    message = mail.EmailMessage(subject, message, from_email, recipient_list,
        connection=connection, headers=headers)
    connection.send_messages([message])
