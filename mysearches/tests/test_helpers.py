def return_file(*args, **kwargs):
    target = 'mysearches/tests/local/'
    if 'nurse' in args[0]:
        target += 'nurse.html'
    elif 'feed' in args[0]:
        target += 'rss.rss'
    elif 'jobs' in args[0]:
        target += 'jobs.html'
    else:
        target += 'other'
    return file(target)

def fake_render_to_string(*args, **kwargs):
    return 'string'
