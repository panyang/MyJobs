import urllib2

from django import template
from django.utils import simplejson as json

register = template.Library()

@register.simple_tag
def degree_select(selected="ba", html_id="",input_name="degree",inc_struc=True):
    """
    Builds an html select list of degree names. The select list is built using
    data stored on a CDN.
    
    Inputs:
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name
    :inc_struc:     whether or not to include the html label and structure
    
    Returns:        
    :html_str:      HTML <select> block
    
    """
    data_url = 'http://js.nlx.org/myjobs/data/degree_list.json'
    data_list = _load_json_data(data_url)
    degree_list = data_list["degrees"];
    try:
        label = data_list["friendly_label"]
    except KeyError:
        label = "Degree"
    
    sel_tag = _build_select_list(degree_list,selected,input_name,html_id)
    
    if inc_struc:
        html_str="<div class='form-label pull-left'>"
        html_str="%s<label for='%s'>%s</label></div>" % (html_str,html_id,label)
        html_str="%s%s<div class='clear'></div>" % (html_str,sel_tag)
    else:
        html_str = sel_tag
        
    return html_str   
    
@register.simple_tag
def country_region_select(selected="can", html_id="", input_name="country",
                          region_html_id="region_selection"):
    """
    Build a Country/Region Section for a form.
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name for country. Region name is locked
                    in order to provide javascript functionality.
    
    """
    selected = selected.lower()
    country_tag = country_select(selected,html_id,input_name,True,region_html_id)
    if country_tag[0] != "<":
        region_tag = ""
    else:
        if selected=="usa":
            default_region="az"
        elif selected=="can":
            default_region="ab"
        else:
            default_region=""
        
        region_tag= region_select(selected,default_region,region_html_id,"region")

    html = country_tag+region_tag
    return html
    
@register.simple_tag
def country_select(selected="usa", html_id="", input_name="country",
                   inc_struc=True,region_html_id=""):
    """
    Builds an html select list of countries. The select list is built using
    data stored on a CDN.
    
    Inputs:
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name
    :child_regions: whether this field has a dependent regions field
    :inc_struc:     whether or not to include the html label and structure
    :region_html_id: the id of a child select block that change with this one.
    
    Returns:        
    :html_str:      HTML <select> block
    
    """
    selected = selected.lower()
    data_url = 'http://js.nlx.org/myjobs/data/countries.json'
    data_list = _load_json_data(data_url)
    country_list = data_list["countries"];
    try:
        label = data_list["friendly_label"]
    except KeyError:
        label = "Country"        
    
    if region_html_id:
        sel_tag = _build_select_list(country_list,selected,input_name,html_id,
                                     "hasRegions",region_html_id)
    else:
        sel_tag = _build_select_list(country_list,selected,input_name,html_id)
    if inc_struc:
        html_str="<div>"
        html_str="%s<label for='%s'>%s</label></div>" % (html_str,html_id,label)
        html_str="%s%s<div class='clear'></div>" % (html_str,sel_tag)
    else:
        html_str = sel_tag
        
    return html_str   

@register.simple_tag
def region_select(country="usa",selected="az",html_id="",input_name="region",
                  inc_struc=True):
    """
    Builds an html select list of regions.
    Inputs:
    :country:       3 letter code of which country's regions to display.
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name
    :inc_struc:     whether or not to include the html label and structure
    
    Returns:        
    :html_str:      HTML <select> block or error message
    
    """
    
    #there is a single file per country, else it returns null.
    country = country.lower()
    selected = selected.lower()
    data_url = 'http://js.nlx.org/myjobs/data/%s_regions.json' % country
    data_list = _load_json_data(data_url)
    try:
        region_list = data_list["regions"]
    except KeyError:
        region_list = {}
        
    try:
        label = data_list["friendly_label"]
    except KeyError:
        label = "Region" 
        
    if "error" in region_list:
        html_str = "<input type='hidden' name='%s' value=''>" % input_name
        html_str = "%sNo regions available for the selected country" % html_str
    elif inc_struc:
        sel_tag = _build_select_list(region_list,selected,input_name,html_id)
        html_str="<div>"
        html_str="%s<label for='%s'>%s</label></div>" %(html_str,html_id,label)
        html_str="%s%s<div class='clear'></div>" % (html_str,sel_tag)
    else:
        html_str = _build_select_list(region_list,selected,input_name,html_id)
        
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
        return {"code":"error","error":"There was an error loading the file."}   
    return json_data
    
def _build_select_list(select_dict,selected,input_name,html_id,class_name="",
                       child_list_id=""):
    """
    Generic function that builds an html select list for the specified type.
    
    Inputs:
    :select_dict:   A dictionary object used to build the <option> nodes
    :selected:      default key to select
    :html_id:       html id to use for the element
    :input_name:    the form element name
    :class_name:    option class name to append to element
    :child_list_id: the id of a child list that changes with this list
    
    Returns:        
    HTML <select> block
    
    """
    attr_str = ""
    if class_name: # assign the class name
        attr_str = " class='%s'" % class_name
    if child_list_id: # store the child id. Used by JavaScript for UI effects
        attr_str = "%s data-childlistid='%s'" % (attr_str, child_list_id)
        
    html_str = "<select name='%s' id='%s'%s>" % (input_name,html_id,attr_str)
    html_str = "%s<option value=''></option>" % html_str
    
    for item in select_dict:
        if item["code"] == "error":
            return item["error"]
        select_flag = ""
        if item["code"].lower() == selected.lower():
            select_flag = " SELECTED"
        if item["code"] != "":
            option_attr = "value='%s'%s" % (item["code"], select_flag)
            html_str = "%s<option %s>%s</option>" % (html_str,option_attr,item["name"])
    html_str = "%s</select>" % html_str    
    return html_str
