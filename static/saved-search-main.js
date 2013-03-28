$(document).ready(function() {
    check_digest_options();
    resize_modal();

    $(window).resize(function() {
        resize_modal();
    });

    function resize_modal() {
        var max_height, margin_top, width, margin_left;
        max_height = $(window).height();
        width = $(window).width();
        if (!is_mobile()) {
            max_height = max_height * 0.8;
            width = width * 0.8;
        }
        margin_top = -(max_height/2);
        margin_left = -(width/2);
        $('#new_modal').css({
            'max-height': max_height.toFixed(0) + 'px',
            'margin-top': margin_top.toFixed(0) + 'px',
            'width': width.toFixed(0) + 'px',
            'margin-left': margin_left.toFixed(0) + 'px',
        });
    }

    function is_mobile() {
        return $(window).width() <= 500;
    }

    $('td.view_search').click(function() {
        var href = $(this).parent().find('.view').prop('href');
        if (is_mobile() && typeof(href) != 'undefined') {
            window.location = href;
        }
    });

    $('#new_btn').click(function(e) {
        if (!is_mobile()) {
            e.preventDefault();
            $('#new_modal').modal();
        }
    });

});

function check_digest_options() {
    // When the user interacts with any fields in the Digest Options form,
    // an ajax request checks that the form is valid and saves the changes
    var timer;
    var pause_interval = 1000;

    $('#id_digest_email').keyup(function() {
        clearTimeout(timer);
        if (form_valid()) {
            timer = setTimeout(save_form, pause_interval);
        }
    });

    $('#id_digest_active').click(function() {
        if (form_valid()) {
            save_form();
        }
    });

    $('#id_send_if_none').click(function() {
        if (form_valid()) {
            save_form();
        }
    });

    function form_valid() {
        $('.digest_error').remove();
        var error;
        if ($('#id_digest_active').prop('checked')) {
            if ($('#id_digest_email').val().length) {
                return true;
            }
        }
        return false;
    }

    function form_status(status) {
        var delay = 5000;
        var timer;
        clearTimeout(timer);
        $('#saved').addClass('label label-info');
        $('#saved').text(status);
        // Fade in 600ms, wait 5s, fade out 600ms
        $('#saved').fadeIn('slow');
        timer = setTimeout('$("#saved").fadeOut("slow")', delay);
    }

    function save_form() {
        var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
            data: { csrfmiddlewaretoken: csrf_token, action: 'save',
                    is_active: $('#id_digest_active').prop('checked')? 'True':'False',
                    email: $('#id_digest_email').val(),
                    send_if_none: $('#id_send_if_none').prop('checked')? 'True':'False' },
            type: 'POST',
            url: '',
            success: function(data) {
                if (data == 'success') {
                    form_status('Saved!');
                } else {
                    form_status('Something went wrong');
                }
            }
        });
    }
};
