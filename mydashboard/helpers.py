import operator
from django.db.models import Q
from urlparse import urlparse

from mydashboard.models import Company, Microsite
from mysearches.models import SavedSearch


def saved_searches(employer, candidate):
    """
    Function that gets employer's companies and those companies microsites.
    Will pull the domain out of the employer_microsites. Gathers the
    candidate's saved search urls and then will pull those urls
    out. Lastly, check to see if employer domains match up with
    candidate domains and return a list of urls.

    inputs:
    :employer:	The employer that is looking at candidate's page
    :candidate:	The job seeker that shows up in employer's activitiy feed

    outputs:
                A list of candidate urls.
    """
    employer_companies = employer.company_set.all()
    employer_microsites = Microsite.objects.filter(
        company__in=employer_companies).values_list('url', flat=True)
    employer_domains = [urlparse(url).netloc for url in employer_microsites]
    candidate_urls = candidate.savedsearch_set.values_list('url', flat=True)
    return [url for url in candidate_urls
            if urlparse(url).netloc in employer_domains]
