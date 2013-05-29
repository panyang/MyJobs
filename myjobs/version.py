"""
Version.py - used to track the version number and build number for the 
My.jobs platform. This file is loaded where the version number is needed.

"""
from datetime import datetime

# Marketing version - requires manual editing every release
marketing_version = "1"

# compute the build number. This a calculated value, based on the number of
# months and days since October 1, 2001. This epoch date is the founding date
# of DirectEmployers Association.
start_str = "01-OCT-2001 00:00:01"
start = datetime.strptime(start_str,"%d-%b-%Y %H:%M:%S")
now = datetime.today()
month_delta = ((now.year-(start.year+1))*12)+(12-start.month+1)+now.month
# generate the build number string
build_calculated = "%s-%s" % (month_delta,now.day)
cache_buster = "%s.%s" % (build_calculated,now.hour)
# generate the full release number (ie 1.0.001-01)
release_number = "%s.%s" % (marketing_version,build_calculated)
