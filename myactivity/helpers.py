import operator
from django.db.models import Q
from urlparse import urlparse

from mydashboard.models import Company, Microsite
from mysearches.models import SavedSearch


def employer_can_view_candidate(employer_domains, candidate):
	"""
	Function that gets employer's companies and those companies microsites.
	Will pull the domain out of the employer_microsites (this moved to view).
	Gathers the candidate's saved search urls and then will pull those domains 
	out as well. Lastly, check to see if employer domains match up with 
	candidate domains.

	inputs:
	:employer_domains:	A list of company's microsite domains owned by the 
						employer
	:candidate:			The job seeker that shows up in employer's activitiy 
						feed

	outputs:
					Boolean expression
	"""
	employer_domains_list = employer_domains
	candidate_urls = candidate.savedsearch_set.values_list('url', flat=True)
	candidate_domains = [urlparse(url).netloc for url in candidate_urls]
	return len(set(employer_domains_list) & set(candidate_domains)) > 0

def candidate_saved_searches_in_view(employer_domains, candidate):
	"""
	Gets the employer domain list and does a filter that filters on the domains

	inputs:
	:employer_domains:	A list of company's microsite domains owned by the 
						employer
	candidate:			The job seeker that shows up in employer's activitiy 
						feed

	outputs:
	:candidate_saved_searches: 	A list of saved searches owned by the candidate
	"""
	employer_domains_list = employer_domains
	candidate_saved_searches = candidate.savedsearch_set.filter(
					reduce(operator.or_, (
					Q(url__contains=domain) for domain in employer_domains)))
	return candidate_saved_searches
