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

/*
Resizes the given modal window.
At mobile resolutions, all modals are fullscreen.
At tablet resolutions, choice modals are not fullscreen
while form and view modals are.
At desktop resolutions, nothing is fullscreen; choice modals
are smaller than form and view modals.

:modal: selector for modal to be resized
*/
function resize_modal(modal) {
    modal = $(modal);
    var window_width = $(window).width();
    var window_height = $(window).height();
    var top_, bottom, left, right;
    var height, max_height;
    var width = 'auto';

    if (window_width <= 1024) {
        left = right = '0px';
        top_ = bottom = '0px';
    } else {
        if (modal.attr('role') !== 'dialog') {
            left = right = '150px';
            top_ = '50px';
            bottom = '100px';
        }
    }

    if (modal.attr('role') === 'dialog') {
        if (window_width <= 500) {
            top_ = bottom = left = right = '0px';
        } else {
            top_ = bottom = (window_height-200)/2;
            left = right = (window_width-500)/2;
            max_height = '150px';
            height = '150x';
            width = '500px';
        }
    } else {
        max_height = window_height - 270;
        height = window_height - 300
    }

    modal.css({'top': top_,
               bottom: bottom,
               left: left,
               right: right,
               margin: 0,
               position: 'fixed',
               width: width,
    })

    modal.find('.modal-body').css({'overflow-y': 'auto',
                                   height: height,
                                   'max-height': max_height,
    });
}
