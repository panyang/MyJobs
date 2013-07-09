from mydashboard.models import Company, Microsite
from mysearches.models import SavedSearch

def company_active_users_with_saved_searches(companies):
	"""
	Grabs all the active users that has saved searches with the list of companies

	Inputs: 
	:companies:		list of company objects

	Outputs:
	:active_users:	a dictionary of active users w/ saved searches for their 
					respective companies
	"""
	active_users = {}
	for company in companies:
		microsites = Microsite.objects.filter(company=company)
		for microsite in microsites:
			searches = SavedSearch.objects.select_related('user')
			searches = searches.filter(url__contains=microsite.company)
			for search in searches:
				active_users.setdefault(company.name, []).append(search.user)
	return active_users

def company_candidate_realtionship(company_active_users, candidate):
	"""
	Looks at the active_users dictionary from company_active_users_with_saved_searches
	and for each company the employer is an administrator to will look through
	the list and see if any users match the candidate aka job seeker's User object.

	Inputs:
	:company_active_users:	dictionary from company_active_users_with_saved_searches
	:candidate:				job seeker's User object	

	Outputs:
							Boolean expression
	"""
	for key in company_active_users.keys():
		company = company_active_users[key]
		for user in company:
			if user == candidate:
				return True
			else:
				return False
