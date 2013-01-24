$(document).ready(function() {
    // collect the csrf token on the page to pass into views with ajax
    csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
    var csrf_token = "";
    if(typeof(csrf_token_tag)!='undefined'){
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }
    register(csrf_token);
    save(csrf_token);

    $(function() {
        $( "input[id$='date']" ).datepicker();
    });
});

function register(csrf_token) {    
    /* When register button is clicked, this triggers an AJAX POST that sends the
       csrf token, the collected email and password fields, and a custom field, 'action'
       that allows the view to differentiate between different AJAX requests.
    */
    $('button#register').click(function(e) {
        e.preventDefault();
        var self = $(this).parents("div.loginBox");
        var form = $('form#registration-form');
        $.ajax({
            type: "POST",
            url: "",
            data: { csrfmiddlewaretoken: csrf_token,
                    action: "register",
                    email: self.find("#id_email").val(),
                    password1: self.find("#id_password1").val(),
                    password2: self.find("#id_password2").val()},
            success: function(data) {
                if (data != 'valid') {
                    // If there are errors, the view returns an updated form with errors
                    // to replace the current one with and we reinitialize the functions
                    form.replaceWith(data);
                    register(csrf_token);
                    buttons();
                } else {
                    // perform the visual transition to page 2
                    $("#titleRow").hide( 'slide',{direction: 'left'},250 );
                    $("#topbar-login").fadeOut(250);
                    setTimeout(function(){                            
                        $("#account-page-2").show('slide',{direction: 'right'},250);
                    }, 250);
                    buttons();
                    clearForm("form#registration-form");
                }
            }
        });
    });
}


function save(csrf_token) {
    $('button#save').click(function(e) {
        e.preventDefault();
        var self = $(this).parents("div#account-page-2");
        var json_data = $('form#profile-form').serialize().replace('=on','=True').replace('=off','=False')+'&action=save_profile';        
        $.ajax({
            type: "POST",
            url: "",
            data: json_data,
            success: function(data) {
                if (data != 'valid') {
                    // If there are errors, the view returns an updated form with errors
                    // to replace the current one with and we reinitialize the functions
                    form.replaceWith(data);
                    save(csrf_token);
                    buttons();
                } else {
                    window.location = '/account';
                }
            }
        });
    });
}

function buttons() {
    // go to next carousel div on click
    $('button#next').click(function(e) {
        e.preventDefault();
        $("#carousel").rcarousel("next");
    });

    // skip to profile page on click
    $('button#profile').click(function(e) {
        e.preventDefault();
        window.location = '/account';
    });
};

function clearForm(form) {
    // clear the inputted form of existing data
    $(':input', form).each(function() {
        var type = this.type;
        var tag = this.tagName.toLowerCase(); // normalize case
        if (type == 'text' || type == 'password' || tag == 'textarea')
            this.value = "";
        else if (type == 'checkbox' || type == 'radio')
            this.checked = false;
        else if (tag == 'select')
            this.selectedIndex = -1;
    });
};
