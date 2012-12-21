$(document).ready(function() {
    // collect the csrf token on the page to pass into views with ajax
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    register(csrf_token);
});

function register(csrf_token) {    
    /* When register button is clicked, this triggers an AJAX POST that sends the
       csrf token, the collected email and password fields, and a custom field, 'action'
       that allows the view to differentiate between different AJAX requests.
    */
    $('button#register').click(function(e) {
        e.preventDefault();
        var self = $(this).parents("div#loginBox");
        var form = $('form#registration-form')
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
