"""
helpers.py
"""
import urllib, hashlib

def gravatar_link(email, size=24):
    """Takes and email address and returns a gravatar pic url or None.
    
    Parameters:
    
    email -- an email address
    size -- the size in pixels
    """
    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    url += urllib.urlencode({'d':'mm', 's':str(size), 'r':'pg'})
    return url

    
    