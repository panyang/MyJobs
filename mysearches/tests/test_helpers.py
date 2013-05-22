def return_file(url, *args, **kwargs):
    """
    Translate a url into a known local file. Reduces the time that tests take
    to complete if they do network access. Replaces `urllib.urlopen`

    Inputs:
    :url: URL to be retrieved
    :args: Ignored
    :kwargs: Ignored

    Outputs:
    :file: File object with a `read()` method
    """
    if 'feed/rss' in url:
        file_ = 'rss.rss'
    elif 'mcdonalds/careers/' in url or \
       url.endswith('?location=chicago&q=nurse'):
        file_ = 'careers.html'
    elif url.startswith('http://jobs.jobs/jobs'):
        file_ = 'jobs.html'
    else:
        file_ = 'other'

    target = 'mysearches/tests/local/'
    target += file_
    return open(target)
