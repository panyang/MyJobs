import urllib2

from django import template
from django.utils import simplejson as json

register = template.Library()

@register.simple_tag
def country_region_select(selected="usa", html_id="", input_name="country"):
    country_tag = country_select(selected,html_id,input_name,True)
    print country_tag[0]
    if country_tag[0] != "<":
        state_tag = ""
    else:
        state_tag = region_select(selected,"","region_selection","region")
        
    html="<div class='form-label pull-left'>"
    html="%s<label for='%s'>Country</label></div>%s" %(html,html_id,country_tag)
    html="%s<div class='clear'></div>" % html
    html="%s<div class='form-label pull-left'>" % html
    html="%s<label for='region_selection'>Region</label>" % html
    html="%s</div>%s" % (html,state_tag)
    return html
    
@register.simple_tag
def country_select(selected="usa", html_id="", input_name="country",
                   child_regions=False):
    """
    Builds an html select list of countries. The select list is built using
    data stored on a CDN.
    
    Inputs:
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name
    :child_regions: whether this field has a dependent regions field
    
    Returns:        
    :html_str:      HTML <select> block
    
    """
    data_url = 'http://js.nlx.org/myjobsdata/countries_full.json'
    country_list = _load_json_data(data_url)
    
    if child_regions:
        html_str = _build_select_list(country_list,selected,input_name,html_id,
                                      "hasRegions")
    else:
        html_str = _build_select_list(country_list,selected,input_name,html_id)
    return html_str

@register.simple_tag
def region_select(country="usa",selected="in",html_id="",input_name="region"):
    """
    Builds an html select list of regions.
    Inputs:
    :country:       3 letter code of which country's regions to display.
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name
    
    Returns:        
    :html_str:      HTML <select> block or error message
    
    """
    
    #there is a single file per country, else it rturns null.
    data_url = 'http://js.nlx.org/myjobsdata/%s_regions.json' % country
    region_list = _load_json_data(data_url)
    if "error" in region_list:
        html_str = "<input type='hidden' name='%s' value=''>" % input_name
        html_str = "%sNo regions available for the selected country" % html_str
    else:
        html_str = _build_select_list(region_list,selected,input_name,html_id)
        
    
    print data_url
    return html_str 

# utility function below here
def _load_json_data(json_url):
    """
    Retrieves an external json file, opens it, and reads it in as a dict.
    
    Inputs:
    :jason_url:     The full url of the json data file, with protocol
    
    Returns:
    :json_data:     Python dictionary version of the json file
    
    """
    try:
        data = urllib2.Request(json_url)
        opener = urllib2.build_opener()
        json_data = json.load(opener.open(data))
    except (urllib2.HTTPError,ValueError):
        return {"error":"There was an error loading the file."}   
    return json_data
    
def _build_select_list(select_dict,selected,input_name,html_id,class_name=""):
    """
    Generic function that builds an html select list for the specified type.
    
    Inputs:
    :select_dict:   A dictionary object used to build the <option> nodes
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name
    :class_name:    option class name to append to element
    
    Returns:        
    HTML <select> block
    
    """
    
    if class_name:
        class_name = " class='%s'" % class_name
    html_str = "<select name='%s' id='%s'%s>" % (input_name,html_id,class_name)    
    for k,v in select_dict.iteritems():
        if k == "error":
            return v
        select_flag = ""
        if k.lower() == selected.lower():
            select_flag = " SELECTED"
        if k != "":
            option_attr = "value='%s'%s" % (k, select_flag)
            html_str = "%s<option %s>%s</option>" % (html_str,option_attr,v)
            
    html_str = "%s</select>" % html_str    
    return html_str