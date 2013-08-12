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
            // redirect to the home page on 403
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
    // protection from cross site requests
    csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
    var csrf_token = "";
    if(typeof(csrf_token_tag)!='undefined'){
       csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }
    data = '&csrfmiddlewaretoken=' + csrf_token + '&';
    data += form.serialize();
    $.ajax({
        type: 'POST',
        url: '/contact/',
        data: data,
        success: function(data) {
            if(data == 'success'){
                window.location.href = "/success/"
            }else{
                var json = jQuery.parseJSON(data);
                // remove color from labels of current errors
                $('[class*=required]').prev().removeClass('required-label');

                // remove border around element
                $('[class*=required]').children().removeClass('required-border');

                // remove current errors
                $('[class*=required]').children().unwrap();

                if($.browser.msie){
                    $('[class*=msieError]').remove()
                }
                for (var index in json.errors) {
                    var $error = $('[class$="'+json.errors[index][0]+'"]');
                    var $field = $('[id$=recaptcha_response_field]')
                    var $labelOfError = $error.prev();
                    // insert new errors after the relevant inputs
                    $error.wrap('<span class="required" />');
                    $error.addClass('required-border')
                    if(!($.browser.msie)){
                        $field.attr("placeholder",json.errors[index][1]);
                        $field.val('');
                    }else{
                        field = $error.parent();
                        field.before("<div class='msieError'><i>" + json.errors[index][1] + "</i></div>");
                    }
                    $labelOfError.addClass('required-label')
                }
            }
        }
    });
}

window.dateFormat = 'dd-M-yy';
