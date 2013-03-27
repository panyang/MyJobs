$(document).ready(function() {
    check_digest_options();
    post_new_search();

    $('tr').click(function() {
        var href = $(this).find('.edit').prop('href');
        if ($(window).width() <= 500 && typeof(href) != 'undefined') {
            window.location = href;
        }
    });

    $('#new_btn').click(function(e) {
        e.preventDefault();
        $('#new_modal').modal();
    });

    $(window).resize(function() {
        var dW;
        var dH;
        if ($(window).width() <= 500) {
            dW = dH = 0;
        } else {
            dW = dH = 0.1;
        }
        var width = $(window).width();
        var margin_w = width * dW;
        var height = $(window).height();
        var margin_h = height * dH;
        $('.modal-body').css('margin', margin_w+'px '+margin_h+'px;');
    });
});

function post_new_search() {
    $('#add_save').click(function() {
        submit();
    });

    function submit() {
        var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[1].value;
        $.ajax({
            data: { csrfmiddlewaretoken: csrf_token, action: 'new_search',
                    feed: $('#id_feed').val(),
                    url: $('#id_url').val(),
                    label: $('#id_label').val(),
                    is_active: $('#id_is_active').prop('checked')? 'True':'False',
                    email: $('#id_email').val(),
                    frequency: $('#id_frequency').val(),
                    day_of_week: $('#id_day_of_week').val(),
                    day_of_month: $('#id_day_of_month').val(),
                    notes: $('#id_notes').val()
            },
            type: 'POST',
            url: '',
            complete: function(data) {
                console.log(data);
                if (data == 'success') {
                } else {
                }
            }
        });

    }
};

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
