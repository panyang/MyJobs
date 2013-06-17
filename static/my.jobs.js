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

// This function will be executed when the user scrolls the page.
$(window).scroll(function(e) {
    // Get the position of the location where the scroller starts.
    var scroller_anchor = $(".scroller_anchor").offset().top;
     
    // Check if the user has scrolled and the current position is after the scroller start location and if its not already fixed at the top 
    if ($(this).scrollTop() >= scroller_anchor && $('#moduleBank').css('position') != 'fixed') 
    {    // Change the CSS of the scroller to hilight it and fix it at the top of the screen.
        $('#moduleBank').css({
            
            'position': 'fixed',
            'top': '0px'
        });
        // Changing the height of the scroller anchor to that of scroller so that there is no change in the overall height of the page.
        $('.scroller_anchor').css('height', '50px');
    } 
    else if ($(this).scrollTop() < scroller_anchor && $('#moduleBank').css('position') != 'relative') 
    {    // If the user has scrolled back to the location above the scroller anchor place it back into the content.
         
        // Change the height of the scroller anchor to 0 and now we will be adding the scroller back to the content.
        $('.scroller_anchor').css('height', '0px');
         
        // Change the CSS and put it back to its original position.
        $('#moduleBank').css({
            
            'position': 'relative'
        });
    }
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
