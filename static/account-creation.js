var current_url = ""; //init current_url as global
$(document).ready(function() {
    // collect the csrf token on the page to pass into views with ajax
    csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
    var csrf_token = "";
    if(typeof(csrf_token_tag)!='undefined'){
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }

    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd"});
    });
    // perform display modifications for fields
    $("#id_name-primary").hide()
    $("label[for=id_name-primary]").hide()
    user_email = "";
    current_url = window.location.pathname;    
});

/* When register button is clicked, this triggers an AJAX POST that sends the
   csrf token, the collected email and password fields, and a custom field, 'action'
   that allows the view to differentiate between different AJAX requests.
*/
$(document).on("click", "button#register", function(e) {
    e.preventDefault();
    var form = $('form#registration-form');
    var json_data = form.serialize()+'&action=register';
    user_email = $("#id_email").val();
    $.ajax({
        type: "POST",
        url: current_url,
        data: json_data,
        success: function(data) {
            try {
                var gravatar_url = jQuery.parseJSON(data).gravatar_url;
                // perform the visual transition to page 2
                $("#id_name-primary").hide()
                $("label[for=id_name-primary]").hide()
                $("#titleRow").hide( 'slide',{direction: 'left'},250 );
                $("#topbar-login").fadeOut(250);
                setTimeout(function(){                            
                    $("#account-page-2").show('slide',{direction: 'right'},250);
                }, 250);
                $("#gravatar").attr("src",gravatar_url);
                buttons();
                clearForm("form#registration-form");
                $(".newUserEmail").html(user_email);                    
            } catch(e) {
                // If there are errors, the view returns an updated form with errors
                // to replace the current one with and we reinitialize the functions
                form.replaceWith(data);
            }
        }
    });
});

$(document).on("click", "button#login", function(e) {
    e.preventDefault();
    var form = $('form#login-form');
    var json_data = form.serialize()+'&action=login';    
    $.ajax({
        type: "POST",
        url: current_url,
        data: json_data,
        success: function(data) {
            if (data != 'valid') {
                form.replaceWith(data);
            } else {
                window.location = '/profile';
            }
        }
    });
    
});

$(document).on("click", "button#save", function(e) {            
    e.preventDefault();
    setPrimaryName();
    var form = $('form#profile-form');
    // replace on and off with True and False to allow Django to validate 
    // boolean fields
    var json_data = form.serialize().replace('=on','=True')
        .replace('=off','=False')+'&action=save_profile';        
    $.ajax({
        type: "POST",
        url: current_url,
        data: json_data,
        success: function(data) {
            if (data != 'valid') {
                form.replaceWith(data);
                $("#id_name-primary").hide()
                $("label[for=id_name-primary]").hide()
            } else {
                window.location = '/profile';
            }
        }
    });
});

// go to next carousel div on click
$(document).on("click", "button#next", function(e) {
    e.preventDefault();
    $("#carousel").rcarousel("next");
});

// skip to profile page on click
$(document).on("click", "button#profile", function(e) {
    e.preventDefault();
    window.location = '/profile';
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
