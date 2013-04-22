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

    $('#delete-account').click(function(){
        var answer = confirm('Are you sure you want to delete your account?');
        if (answer == true) {
            window.location = '/account/delete';
        }
    });

    $('#disable-account').click(function(){
        var answer = confirm('Are you sure you want to disable your account?');
        if (answer == true) {
            window.location = '/account/disable';
        }
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

function resize_modal(modal) {
    var window_width = $(window).width();
    var window_height = $(window).height();
    var top_, bottom, left, right;
    var height, max_height;

    if (window_width <= 1024) {
        left = right = '1%';
        top_ = bottom = '1%';
    } else {
        left = right = '150px';
        top_ = '50px';
        bottom = '100px';
    }

    max_height = window_height - 270;

    height = window_height - 300;

    $(modal).css({ 'top': top_,
                   bottom: bottom,
                   left: left,
                   right: right,
                   margin: 0,
                   position: 'fixed',
                   width: 'auto',
    });

    $(modal).find('.modal-body').css({ 'overflow-y': 'auto',
                                       height: height,
                                       'max-height': max_height,
    });
}
