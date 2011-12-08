from django.core.mail import send_mail
from smtpailheader import SmtpApiHeader

global COUNT
COUNT = 1
to = ['mike@seidle.net', 'mike@directemployers.com', 'rick@directemployers.com']

def send_test (s = "subject ", m = "Message text, baby", f="admin@my.jobs", t=['mike@directemployers.com']):
      global COUNT
      s = s + COUNT.__str__()
      r = send_mail(s, m, f, t, fail_silently=False)
      COUNT +=1
      return r

subject = "DE Test message"
message_text = "Here's an email message sent via SendGrid.\n\n\nw00000t!"

send_test(s=subject, m=message_text, t=to)
