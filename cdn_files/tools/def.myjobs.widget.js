$(document).ready(function(){    
    var str = '<link rel="stylesheet" type="text/css" ';
    str+='href="//d2e48ltfsb5exy.cloudfront.net/myjobs/tools/widget/def.myjobs.widget.css">'; 
    str+= '<div id="direct_savedsearch"><a href="https://secure.my.jobs/">';
    str+= '<h3>Save This Search</h3></a>';
    str += '<div id="savedsearch_form"></div><em class="subtext">Cancel ';
    str+= 'Anytime</em></div></div>';
    document.getElementById('de-myjobs-widget').innerHTML = str;

    form = savedsearch_object($("#savedsearch_form"));
    form.create_form(form);
});

function savedsearch_object(ss_box){
    /*
    Create a saved search form object. This is an object that is a self-contained
    widget that generates the form and handles the AJAX calls back and forth w/
    the my.jobs API.
    
    Methods:
    :create_form:   Generated the the saved search form
    :ajax_save:     Client side email validation and then calls the my.jobs
                    API. It then handles the return object.
                    
    Inputs:
    :ss_box:    jQuery DOM object of the containing box.
    
    Returns:
    :ssearch:   the saved search widget object
    
    Noted Technical Debt
    --------------------
    This function does not deal with cookies or preservation of saved search
    state for a given URL. There are some key problems that need to be dealt
    with:
        1. How do determine if a saved search has been deleted on my.jobs
        2. How to check against my.jobs for saved search status without sending
           an ajax request on every page load (eek!).       
    Most likely, we need to build a full login system to accomodate the 
    above instead of the automated system this feature uses. This will 
    require the building of a django app to handle direct authentication
    against my.jobs. Until then, the user will always be presented with the form,
    even if they have already created a saved search for that url.
    */
    var ssearch = {};
    // HTML for the form
    var ss_form = '<form onsubmit="return false;">';
    ss_form += '<label for="savedsearch_email">Get new jobs sent directly to ';
    ss_form += 'your inbox!</label>';
    ss_form += '<input placeholder="Your email address" type="text" ';
    ss_form += 'id="savedsearch_email" name="savedsearch_email"/>';
    ss_form += '<button id="savedsearch_button">Save This Search</button></form>';
    // HTML for successful save (new user)
    str = '<em class="success">Success</em><p>We will send you results from ';
    str+= 'this search to <b>****</b> once per day. You can manage this saved ';
    str+= 'search at <a href="http://my.jobs/" target="_blank">My.jobs</a>.</p>';
    str+= '<p>Check your email for login and email verification instructions.</p>';
    ssearch.new_user_msg = str;
    // HTML for successful save (existing user)
    str = '<em class="success">Success</em><p>We will send you results from this search to <b>****</b> once ';
    str+= 'per day. You can manage this saved search by logging in to ';
    str+= '<a href="http://my.jobs/" target="_blank">My.jobs</a>.</p>';
    ssearch.existing_user_msg = str;
    // HTML for pre-existing saved search
    str = '<em class="warning">Saved Search Exists!</em><p>There is already a ';
    str+= 'saved search for this url for <b>****</b>. To edit that saved search';
    str+= ', <a href="http://my.jobs/" target="_blank">please login to ';
    str+= 'My.jobs</a>.</p><p><button id="reset_savedsearch">Try a different ';
    str+= 'email</button></p>';
    ssearch.existing_search_msg = str;
    // HTML for save error
    str = '<em class="warning">Something went wrong!</em><p>Please try again.';
    str+= '</p><p><button id="reset_savedsearch">Try again</button></p>';
    ssearch.save_error_msg = str;
    // HTML displayed while saving
    ssearch.loading_text = '<em class="loading">Saving this search</em>';
    // HTML displayed when there is an error 
    ssearch.email_error = '<em class="fielderror">Please provide a valid email address</em>';

    ssearch.new_form = ss_form;
    ssearch.box = ss_box;
    ssearch.new_user = false;
    ssearch.msg = "";
    ssearch.email = "";
    ssearch.api_root = "http://secure.my.jobs:80"

    ssearch.create_form = function(obj){
        obj.box.hide();
        obj.box.html(obj.new_form);
        obj.box.submit(function(){obj.ajax_save(obj)});
        obj.box.fadeIn();
        $('#savedsearch_email').placeholder();
    }
    ssearch.ajax_save = function(obj){
        var ss_email = $("#savedsearch_email").val();
        var ss_username = "directseo@directemployersfoundation.org";
        var ss_api_key = "6fcd589a4efa72de876edfff7ebf508bedd0ba3e";
        var ss_api_str = "&username=" + ss_username 
                         + "&api_key=" + ss_api_key;
        
        create_ss = function(data) {
            /*
            Send the request to create a new saved search object.

            Inputs:
            :data:    JSON encoded data passed from API
            */
            if(data.user_created) {
                obj.msg = obj.new_user_msg.replace("****", data.email);
                obj.new_user = true;
            }
            else {
                obj.msg = obj.existing_user_msg.replace("****", data.email);
            }

            $.ajax({
                url: obj.api_root 
                    + "/api/v1/savedsearch/?callback=finish_ss&email="
                    + data.email + "&url=" + ss_url + ss_api_str,
                dataType: "jsonp",
                type: "GET",
                crossDomain: true,
                jsonp: false,
                processData: false,
                headers: {
                    'Content-Type': "application/json", 
                    Accept: 'text/javascript'
                },
            });
        }
        finish_ss = function(data) {
            /*
            Reloads saved searchform based on response to request to create
            a new saved search.

            Inputs:
            :data:    JSON encoded data passed from API
            */
            obj.box.hide();
            enable_reset = false;
            // For new searches
            if(data.new_search) {
                ss_done = obj.msg;
            }
            else {
            // For existing searches
                ss_done = obj.existing_search_msg.replace("****", data.email);
                enable_reset = true;
            }
            if(data.error) {
                obj.handle_error(obj);
            }
            else {
                obj.update_form(obj, ss_done, enable_reset);
            }            
        }

        obj.email = ss_email;
        if(validate_email(ss_email)){
            ss_url = window.location.toString();
            ss_url = encodeURIComponent(ss_url);
            obj.box.hide();
            obj.box.html(obj.loading_text);
            obj.box.fadeIn();
            obj.cachekey = "&cachekey="+(new Date).getTime()

            // Initial request to create new user or confirm existing user
            $.ajax({
                url: obj.api_root 
                    + "/api/v1/user/?callback=create_ss&email=" 
                    + ss_email + ss_api_str,
                dataType: "jsonp",
                type: "GET",
                crossDomain: true,
                jsonp: false,
                processData: false,
                headers: {
                    'Content-Type': "application/json", 
                    Accept: 'text/javascript'
                },
            });
        }
        else {
            obj.box.children(".fielderror").remove();
            $("#savedsearch_email").after(obj.email_error);
        }
    }
    ssearch.handle_error = function(obj){
        obj.box.html(obj.save_error_msg);
        obj.box.fadeIn();
        $("#reset_savedsearch").click(function(){obj.create_form(obj)});
    }
    ssearch.update_form = function(obj,ss_done,enable_reset){
        obj.box.html(ss_done);
        obj.box.fadeIn();        
        if(enable_reset){
            $("#reset_savedsearch").click(function(){obj.create_form(obj)});
        }
    }
return ssearch;
}