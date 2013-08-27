from bs4 import BeautifulSoup as Soup
import json
from datetime import datetime
from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.utils.encoding import smart_str, smart_unicode

from myjobs.decorators import user_is_allowed
from myjobs.models import User
from mydashboard.models import Company

from django.conf import settings

import urllib2
from urlparse import urlparse, urlunparse, parse_qs
from urllib import urlencode

user_is_allowed()
user_passes_test(User.objects.is_active)
user_passes_test(User.objects.not_disabled)
def analytics_main(request):
    search_id = int(request.REQUEST.get('company'))
    company_obj = Company.objects.get(pk=search_id)
    
    search_url = "http://50.19.85.235:8983/solr/select/?q=company:%s&rows=20" % company_obj.name
    
    search_xml = urllib2.urlopen(search_url).read()
    xml_soup = Soup(search_xml)
    #print xml_soup
    buid_data=[]
    job_list=[]
    for doc in xml_soup.findAll('doc'):
        for node in doc.findAll('long'):
            if node.attrs['name']=='buid':
                if not node in buid_data:
                    buid_data.append(node)
        job_title = ""
        job_desc = ""
        for node in doc.findAll('str'):
            if node.attrs and node.attrs['name']=="title":
                job_title = node.contents[0]
            if node.attrs and node.attrs['name']=="html_description":
                job_desc = node.contents[0]
        if job_title:
            job_list.append({'title':job_title,'description':job_desc})

    buid_json = []
    total_jobs = 0;
    for buid in buid_data:
        #print buid.contents[0]
        ms_api = "http://jobs.jobs/api/v1/business_unit/%s?username=%s&api_key=%s&format=json" % (buid.contents[0], settings.SEO_READ_USER, settings.SEO_READ_KEY)
        print ms_api
        ms_result = json.loads(urllib2.urlopen(ms_api).read())
        buid_json.append({'buid':buid.contents[0],'count':ms_result['associated_jobs']})
        total_jobs+=ms_result['associated_jobs']
    buid_json.append({'buid':'All','count':total_jobs})
    

    job_json = []
    for job in job_list:
        job_json.append({"title":job["title"],'description':job["description"]})
    print job_json
    #return HttpResponse (job_list)
    return render_to_response('myanalytics/analytics_main.html',
                              {
                                'job_sources': buid_json, 
                                'job_list': job_json,
                                'view_name': 'Analytics',
                                'company':company_obj},
                              RequestContext(request))
