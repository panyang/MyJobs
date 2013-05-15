/******
Document Level Actions
*******/
$(document).ready(function(){
    var offset = 0;
    
    /*Explicit control of main menu, primarily for mobile but also provides
    non hover and cover option if that becomes an issue.*/
    $("#nav .main-nav").click(function(){
        $("#nav").toggleClass("active");
        return false;
    });
    $("#pop-menu").mouseleave(function(){
        $("#nav").removeClass("active");
    });

    $('#disable-account').click(function(){
        var answer = confirm('Are you sure you want to disable your account?');
        if (answer == true) {
            window.location = '/account/disable';
        }
    });


    $('.show-captcha-modal').click(function(e) {
        e.preventDefault();
        $.ajax({
            type:"POST",
            url: "/edit/delete",
            data: $("#captcha-form").serialize(),
            success: function(data) {
                if (data == 'success') {
                    $("#captcha-errors").html('');
                    $("#captcha_modal").modal();
                } else {
                    var error = jQuery.parseJSON(data)[0][0];
                    $("#captcha-errors").html('<div class="alert-message block-message error">'+error+'</div>');
                }
            }
        });
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
