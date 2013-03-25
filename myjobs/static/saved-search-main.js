$(document).ready(function() {
    check_digest_options();
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
        if ($('#id_digest_active').prop('checked')) {
            if ($('#id_digest_email').length) {
                return true;
            }
        }
        return false;
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

        function form_status(status) {
            $('#saved').addClass('label label-info');
            $('#saved').text(status);
            $('#saved').fadeIn().fadeOut('slow');
        }
    }
};
