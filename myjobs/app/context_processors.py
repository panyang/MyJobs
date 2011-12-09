from django.conf import settings
from django.contrib.sites.models import Site


def current_site_info(request):
    """Retrieves site info from djang.contrib.sites

    Adds the following to the context:

    site_name -- the site name
    site_domain -- the site's domain
    """
    
    try:
        current_site = Site.objects.get_current()
        values = {
            'site_domain': current_site.domain,
            'site_name': current_site.name,
        }
        return values
    except Site.DoesNotExist:
        # Return empty strings in case template needs context vars
        values = {'site_domain':'', 'site_name':''}
        return values
