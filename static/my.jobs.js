/******
Document Level Actions
*******/
$(document).ready(function(){
    var offset = 0;

    $(this).ajaxStart(function () {
        // Disable errant clicks when an ajax request is active
        // Does not prevent the user from closing the modal
        $('button').attr('disabled', 'disabled');
        $('[id$="modal"] a').attr('disabled', 'disabled');

        // Show ajax processing indicator
        $("#ajax-busy").show();
        $("#ajax-busy").show();   
    });
    $(this).ajaxStop(function () {
        // Allow button clicks when ajax request ends
        $('button').removeAttr('disabled');
        $('[id$="modal"] a').removeAttr('disabled');

        // Hide ajax processing indicator
        $("#ajax-busy").hide();
        $(this).dialog("close");
    });
    $(this).ajaxError(function (e, xhr) {
        if (xhr.status == 403) {
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

    $('#disable-account').click(function(){
        var answer = confirm('Are you sure you want to disable your account?');
        if (answer == true) {
            window.location = '/account/disable';
        }
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
