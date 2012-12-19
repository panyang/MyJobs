$(document).ready(function() {
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $( "#carousel" ).rcarousel({width: 960, height: 600,
                                visible:1, step:1} );
    register(csrf_token);
});

function register(csrf_token) {    
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
                    form.replaceWith(data);
                    register(csrf_token);
                    buttons();
                } else {
                    $("#carousel").rcarousel("next");
                    buttons();
                    clearForm("form#registration-form");
                }
            }
        });
    });
}

function buttons() {
    $('button#next').click(function(e) {
        e.preventDefault();
        $("#carousel").rcarousel("next");
    });

    $('button#profile').click(function(e) {
        e.preventDefault();
        window.location = '/account';
    });
};

function clearForm(form) {
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
