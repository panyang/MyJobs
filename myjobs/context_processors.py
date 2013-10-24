from django.conf import settings
from django.contrib.sites.models import Site


def current_site_info(request):
    """Retrieves site info from djang.contrib.sites

    Adds the following to the context:

    site_name -- the site name
    site_domain -- the site's domain
    description -- gives the site a description
    keywords -- key words for SEO
    """
    
    try:
        current_site = Site.objects.get_current()
        values = {
            'domain': current_site.domain,
            'site_name': current_site.name,
            'description': 'My.jobs is a platform that was designed to make' \
                        ' finding emplyoment easier. Job seekers can control their data,' \
                        ' and then making it easy for them to connect to like minded and' \
                        ' interested employers.',
            'keywords': 'jobs,job,find job,my jobs,job search,employment,employers,saved search,search agent',
        }
        return values
    except Site.DoesNotExist:
        # Return empty strings in case template needs context vars
        values = {'site_domain':'', 'site_name':'', 'description':'', 'keywords':'',}
        return values
