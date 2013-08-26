/******
Document Level Actions
*******/
$(document).ready(function(){
    $("#id_email").attr("placeholder", "Email");
    $( "input[id$='date']" ).datepicker({dateFormat: window.dateFormat,
                                         constrainInput: false});

    var offset = 0;

    $(this).ajaxStart(function () {
        // Disable errant clicks when an ajax request is active
        // Does not prevent the user from closing the modal
        $('button').attr('disabled', 'disabled');
        $('a.btn').attr('disabled', 'disabled');

        // Show ajax processing indicator
        $("#ajax-busy").show();
        $("#ajax-busy").show();   
    });
    $(this).ajaxStop(function () {
        // Allow button clicks when ajax request ends
        $('button').removeAttr('disabled');
        $('a.btn').removeAttr('disabled');

        // Hide ajax processing indicator
        $("#ajax-busy").hide();
        $(this).dialog("close");
    });
    $(this).ajaxError(function (e, xhr) {
        if (xhr.status == 403 || xhr.status == 404) {
            /*
            Redirects the user to the home page when various error types occur
            403: the user is trying to access a protected page but is not
                logged in
            404: the user is trying to access a page using another user's
                email address
            */
            window.location = '/';
        }
    });
    
    /*Explicit control of main menu, primarily for mobile but also provides
    non hover and cover option if that becomes an issue.*/
    $("#nav .main-nav").click(function(){
        $("#nav").toggleClass("active");
        return false;
    });
    $("#pop-menu").mouseleave(function(){
        $("#nav").removeClass("active");
    });

    $('a.account-menu-item').click(function(e) {
        e.preventDefault();
        if ($(window).width() < 500) {
            $('div.settings-nav').hide();
            $('div.account-settings').show();
        }
    });
    
    $(function() {
        $('input, textarea').placeholder();
    });

    $('#captcha-form').submit(function(e) {
        e.preventDefault();
        contactForm();
    });
    
    $("#newAccountData").change(function() {
        // Calculates the profile completion level every time a field on
        // the new account profile form is changed.
        
        profile_completion = 0;
        if($("#id_name-given_name").val() != "" && $("#id_name-family_name").val() != "") {
            profile_completion += (100/5);
        }
        if($("#id_edu-organization_name").val() != "" && $("#id_edu-degree_date").val() != "" &&
           $("#id_edu-education_level_code").val() >= 3 && $("#id_edu-degree_name").val() != "") {
            profile_completion += (100/5);
        }
        if ($("#id_ph-area_dialing").val() != "" || $("#id_ph-number").val() != "" ||
            $("#id_ph-extension").val() != "" || $("#id_ph-use_code").val() != "") {
            profile_completion += (100/5);
        }
        if ($("#id_addr-address_line_one").val() != "" || $("#id_addr-address_line_two").val() != "" ||
            $("#id_addr-city_name").val() != "" || $("#id_addr-country_sub_division_code").val() != "" ||
            $("#id_addr-country_code").val() != "" || $("#id_addr-postal_code").val() != "") {
            profile_completion += (100/5);
        }
        
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
    })
});
             
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

// Validation for contact form
function contactForm(){
    var form = $('#captcha-form');

    var data = form.serialize();
    $.ajax({
        type: 'POST',
        url: '/contact/',
        data: data,
        dataType: 'json',
        success: function(data) {
            if(data.validation == 'success'){
                $('#contact-form').hide('slide', {direction: 'left'}, 250);
                setTimeout(function(){
                    $('#success-info').show('slide', {direction: 'right'}, 250);
                    $('.formBox').show('slide', {direction: 'right'}, 250);
                }, 300);
                $('#name-input').html(data.name);
                $('#email-input').html(data.c_email);
                if(data.phone == ''){
                    $('#phone-input').html('Not provided');
                }else{
                    $('#phone-input').html(data.phone);
                }
                $('#iam-input').html(data.c_type);
                $('#aoi-input').html(data.reason);
                $('#comment-input').html(data.comment);
                $('#time-input').html(data.c_time);
            }else{
                var required = $('[class*=required]');
                // remove color from labels of current errors
                required.prev().removeClass('required-label');

                // remove border around element
                required.children().removeClass('required-border');

                // remove current errors
                required.children().unwrap();

                if($.browser.msie){
                    $('[class*=msieError]').remove()
                }
                for (var index in data.errors) {
                    var $error = $('[class$="'+data.errors[index][0]+'"]');
                    var $field = $('[id$=recaptcha_response_field]')
                    var $labelOfError = $error.prev();
                    // insert new errors after the relevant inputs
                    $error.wrap('<div class="required" />');
                    $error.addClass('required-border')
                    if(!($.browser.msie)){
                        $field.attr("placeholder",data.errors[index][1]);
                        $field.val('');
                    }else{
                        field = $error.parent();
                        field.before("<div class='msieError'><i>" + data.errors[index][1] + "</i></div>");
                    }
                    $labelOfError.addClass('required-label')
                }
            }
        }
    });
}

window.dateFormat = 'dd-M-yy';
