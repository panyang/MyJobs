from sendgrid import SmtpApiHeader
import json
 
hdr = SmtpApiHeader()
receiver = ['kyle@somewhere.com','bob@someplace.net','someguy@googlemailz.coms']
times = ['1pm', '2pm', '3pm']
names = ['kyle', 'bob', 'someguy']
 
hdr.addTo(receiver)
hdr.addSubVal('-time-', times)
hdr.addSubVal('-name-', names)
hdr.addFilterSetting('subscriptiontrack', 'enable', 1)
hdr.addFilterSetting('twitter', 'enable', 1)
hdr.setUniqueArgs({'test':1, 'foo':2})
a = hdr.asJSON()
a = hdr.as_string()
print a
