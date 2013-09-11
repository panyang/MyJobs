var current_url = ""; //init current_url as global
var profile_url = "/profile/";
$(document).ready(function() {
    $( "input[id$='date']" ).datepicker({dateFormat: window.dateFormat,
                                                     constrainInput: false});

    // perform display modifications for fields on initial profile form
    $("#newAccountData #id_name-primary").hide()
    $("#newAccountData label[for=id_name-primary]").hide()
    current_url = '/';
});

/* When register button is clicked, this triggers an AJAX POST that sends the
   csrf token, the collected email and password fields, and a custom field, 'action'
   that allows the view to differentiate between different AJAX requests.
*/
$(document).on("click", "button#register", function(e) {
    e.preventDefault();
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var form = $('form#registration-form');
    var json_data = form.serialize()+'&action=register&csrfmiddlewaretoken='+csrf_token;
    user_email = $("#id_email").val();
    $.ajax({
        type: "POST",
        url: current_url,
        data: json_data,
        global: false,
        success: function(data) {
            /*
            The output in this data is a little different than the rest.
            This one outputs errors, when there are errors. But on success,
            outputs a gravatar url, instead of 'valid' or 'success'.
            */
            var json = jQuery.parseJSON(data);
            // Check to see if json.gravatar_url is present, in this case, success.
            if (Boolean(json.gravatar_url)){
                var gravatar_url = json.gravatar_url;
                // perform the visual transition to page 2
                $("#id_name-primary").hide()
                $("label[for=id_name-primary]").hide()
                $("#titleRow").hide( 'slide',{direction: 'left'},250 );
                $("#topbar-login").fadeOut(250);
                setTimeout(function(){                            
                    $("#account-page-2").show('slide',{direction: 'right'},250);
                }, 250);
                $("#gravatar").append(gravatar_url);
                clearForm("form#registration-form");
                $(".newUserEmail").html(user_email); 
            }else{
                // Remove all required field changes, if any
                removeRequiredChanges();

                // For every error passed by json, run jsonError function
                for (var index in json.errors) {
                    jsonErrors(index, json.errors);
                }
            }
        }
    });
});

$(document).on("click", "button#login", function(e) {
    e.preventDefault();
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var form = $('form#login-form');
    var json_data = form.serialize()+'&action=login&csrfmiddlewaretoken='+csrf_token;
    $.ajax({
        type: "POST",
        url: current_url,
        data: json_data,
        global: false,
        success: function(data) {
            // converts json to javascript object
            var json = jQuery.parseJSON(data);
            if (json.validation != 'valid') {
                // Remove all required field changes, if any
                removeRequiredChanges();

                // For every error passed by json, run jsonError function
                for (var index in json.errors) {
                    jsonErrors(index, json.errors);
                }
            } else {
                if(json.url == 'undefined'){
                    window.location = profile_url;
                }else{
                    window.location = json.url;
                }           
            }
        }
    });
    
});

$(document).on("click", "button#save", function(e) {            
    e.preventDefault();
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    setPrimaryName();
    var form = $('form#profile-form');
    // replace on and off with True and False to allow Django to validate 
    // boolean fields
    var json_data = form.serialize().replace('=on','=True')
        .replace('=off','=False')+'&action=save_profile&csrfmiddlewaretoken='+csrf_token;        
    $.ajax({
        type: "POST",
        url: current_url,
        data: json_data,
        global: false,
        success: function(data) {
            if (data != 'valid') {
                form.replaceWith(data);
                $("#id_name-primary").hide()
                $("label[for=id_name-primary]").hide()
                $( "input[id$='date']" ).datepicker({dateFormat: window.dateFormat,
                                                 constrainInput: false});
            } else {
                window.location = profile_url;
            }
        }
    });
});

$(document).on("change", "#newAccountData", function() {
    // Calculates the profile completion level every time a field on
    // the new account profile form is changed.
     
    profile_completion = 0;
    if($("#id_name-given_name").val() != "" && $("#id_name-family_name").val() != "") {
        profile_completion += 1;
    }
    if($("#id_edu-organization_name").val() != "" && $("#id_edu-degree_date").val() != "" &&
       $("#id_edu-education_level_code").val() >= 3) {
        profile_completion += 1;
    }
    if ($("#id_ph-area_dialing").val() != "" || $("#id_ph-number").val() != "" ||
        $("#id_ph-extension").val() != "" || $("#id_ph-use_code").val() != "") {
        profile_completion += 1;
    }
    if ($("#id_addr-address_line_one").val() != "" || $("#id_addr-address_line_two").val() != "" ||
        $("#id_addr-city_name").val() != "" || $("#id_addr-country_sub_division_code").val() != "" ||
        $("#id_addr-country_code").val() != "" || $("#id_addr-postal_code").val() != "") {
        profile_completion += 1;
    }
    if($("#id_work-position_title").val() != "" && $("#id_work-organization_name").val() != "" &&
       $("#id_work-start_date").val() != "") {
        profile_completion += 1;
    }
    
    profile_completion = Math.round((profile_completion/num_modules)*100);
    
    bar = "bar ";
    if(profile_completion <= 20) {
        bar += "bar-danger";
    }
    else if(profile_completion <= 40) {
        bar += "bar-warning";
    }
    else if(profile_completion <= 60) {
        bar += "bar-info";
    }
    else {
        bar += "bar-success";
    }
    
    $("#initial-bar").removeClass();
    $("#initial-bar").addClass(bar);
    
    $("#initial-bar").css("width", profile_completion + "%");
    $(".initial-highlight").text(profile_completion + "% complete");
});

// go to next carousel div on click
$(document).on("click", "button#next", function(e) {
    e.preventDefault();
    $("#carousel").rcarousel("next");
});

// skip to profile page on click
$(document).on("click", "button#profile", function(e) {
    e.preventDefault();
    window.location = profile_url;
});

function setPrimaryName(){
    /**
    Detects if a value hasbeen entered in either name form and sets the hidden
    checkmark field for priamry to true (since this is the users only name
    at this point. This prevents false validation errors when the form is empty.    
    **/    
    first_name = $("#id_name-given_name").val();
    last_name = $("#id_name-family_name").val();
    if(first_name!=""||last_name!=""){
        $("#id_name-primary").attr("checked","checked");
    }else{
        $("#id_name-primary").attr("checked",false);
    }
}

function removeRequiredChanges(){
    // remove current errors
    $('[class*=required-border]').css('border', '');
    $('[class*=required-border]').removeClass('required-border');

    // remove IE specific errors, if IE
    if($.browser.msie){
        $('[class*=msieError]').remove();
    }
}

function jsonErrors(index, errors){
    /*
    Gets errors and adds front-end attributes and styling to show the user
    what went wrong with their form. Shows error messages in placeholders for
    bowsers with the exception of IE. IE messages are displayed above the field
    that has the error.

    This function in most cases will be ran in conjunction with a for loop.

    :index:     Is an integer, comes from the iterated value from a for loop.
    :errors:    Parsed json that has the label "errors". Errors is a 
                'multidimensional array' {errors:[key][value]}
    */
    var $error = $('[id$="_'+errors[index][0]+'"]');
    var $labelOfError = $error.parent().prev();
    // insert new errors after the relevant inputs
    if($.browser.msie){
        field = $error.parent().prev();
        field.before("<div class='msieError'><i>" + errors[index][1] + "</i></div>");
    }else{
        $error.addClass('required-border');
        $error.val('');
        $error.attr("placeholder",errors[index][1]);
    }
    $error.css('border', '1px solid #D00')
}
