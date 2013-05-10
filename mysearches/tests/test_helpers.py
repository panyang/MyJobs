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
    url_file_map = {'http://jobs.jobs/jobs': 'jobs.html',
                    '?location=chicago&q=nurse': 'careers.html',
                    'mcdonalds/careers/': 'careers.html',
                    'feed/rss': 'rss.rss'}

    default = 'other'

    target = 'mysearches/tests/local/'
    try:
        value = next(v for (k,v) in url_file_map.iteritems()
                         if url.endswith(k))
    except StopIteration:
        value = default
    target += value
    return open(target)

def fake_render_to_string(*args, **kwargs):
    """
    Returns a static string. Reduces the time that it takes to render emails,
    which seems to be much greater than the time to render normal templates

    Inputs:
    :args: Ignored
    :kwargs: Ignored

    Outputs:
    :string: Easily-computed string value
    """
    return 'string'
