$(document).ready(function() {
    check_digest_options();
    save_new_form();
    resize_modal();
    add_valid_label();
    disable_fields();

function disable_fields() {
    // Disable/hide fields until valid URL is entered
    if ($("#id_url").val().length == 0 ) {
        $('#id_label').attr("disabled", "disabled");
        $('#id_label').hide();
        $('#id_is_active').attr("disabled", "disabled");
        $('#id_is_active').hide();
        $('#id_email').attr("disabled", "disabled");
        $('#id_email').hide();
        $('#id_frequency').attr("disabled", "disabled");
        $('#id_frequency').hide();
        $('#id_notes').attr("disabled", "disabled");
        $('#id_notes').hide();
        $('#id_day_of_week').attr("disabled", "disabled");
        $('#id_day_of_week').hide();
        $('#id_day_of_month').attr("disabled", "disabled");
        $('#id_day_of_month').hide();
        $('label[for="id_frequency"]').hide();
        $('label[for="id_email"]').hide();
        $('label[for="id_is_active"]').hide();
        $('label[for="id_label"]').replaceWith('&nbsp;');
        $('label[for="id_notes"]').hide();
        $('#add_save').hide();
    }
}

    validate_url();

    $(window).resize(function() {
        resize_modal();
    });

    $('#new_modal').on('hidden', function() {
        clearForm($('form#saved-search-form'));
        disable_fields();
        $('.alert-message.block-message.error').remove();
        $('#id_url').blur();
        $('#validated').replaceWith('&nbsp;');
    });

    function resize_modal() {
        var max_height, margin_top, width, margin_left;
        max_height = $(window).height();
        width = $(window).width();
        if (!is_mobile()) {
            max_height = max_height * 0.8;
            width = width * 0.6;
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
        e.preventDefault();
        $('#new_modal').modal();
    });

});

function validate_url() {
    // When user stops typing, an ajax request is sent to Django where it checks for
    // the validity of the URL. If it's valid, it informs the user and unblocks the
    // remaining fields.
    var timer;
    var pause_interval = 1000;

    // Known Firefox/Opera bug: this captures presses of the Esc key
    $('#id_url').on('keypress cut paste input', function(){
        clearTimeout(timer);
        if ($('#id_url').val) {
            timer = setTimeout(validate, pause_interval);
        }
    });

    function validate () {
        var csrf_token = $('#saved-search-form input[name=csrfmiddlewaretoken]').val();
        var form = $('form');
        var url = $("#id_url").val(); 
        validation_status('Validating...')
        $.ajax({
            type: "POST",
            url: "",
            data: { csrfmiddlewaretoken: csrf_token,
                    action: "validate",
                    url: url},
            success: function(data) {
                var json = jQuery.parseJSON(data);
                if (json.url_status == 'valid') {
                    validation_status(json.url_status);
                    enable_fields();
                    date_select();
                    if ($('#id_label').val().length == 0) {
                        $("#id_label").val(json.feed_title);
                    }
                    if ($('#id_feed').val().length == 0) {
                        $("#id_feed").val(json.rss_url);
                    }
                }
                else {
                    validation_status(json.url_status);
                }
            }
        });

        function enable_fields() {
            $('#id_label').removeAttr("disabled");
            $('#id_label').show();
            $('#id_is_active').removeAttr("disabled");
            $('#id_is_active').show();
            $('#id_email').removeAttr("disabled");
            $('#id_email').show();
            $('#id_frequency').removeAttr("disabled");
            $('#id_frequency').show();
            $('#id_notes').removeAttr("disabled");
            $('#id_notes').show();
            $('#id_day_of_week').removeAttr("disabled");
            $('#id_day_of_week').show();
            $('#id_day_of_month').removeAttr("disabled");
            $('#id_day_of_month').show();
            $('label[for="id_frequency"]').show();
            $('label[for="id_email"]').show();
            $('label[for="id_is_active"]').show();
            $('label[for="id_notes"]').show();
            $('#add_save').show();
        }

        function validation_status(status) {
            var label_text;

            if (status == 'valid') {
                label_text = 'label label-success';
            } else {
                label_text = 'label label-important';
            }
            if ($("#validated").length) {
                $('#validated').removeAttr('class');
                $('#validated').addClass(label_text);
                $("#validated").text(status);
            } else {
                form.find("#validated_label").after(' <div id="validated" class="'+label_text+'">'+status+'</div>');
            }
        };
    }
};

function check_digest_options() {
    // When the user interacts with any fields in the Digest Options form,
    // an ajax request checks that the form is valid and saves the changes
    var timer;
    var pause_interval = 1000;

    $('#digest_submit').click(function(e) {
        e.preventDefault();
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

function save_new_form() {
    $('#add_save').click(function() {
        save_form();
    });

    function save_form() {
        var csrf_token = $('#saved-search-form input[name=csrfmiddlewaretoken]').val();
        var is_active = $('#id_is_active').prop('checked')? 'True':'False';
        var form = $('form#saved-search-form fieldset');
        $.ajax({
            data: { action: "new_search",
                    csrfmiddlewaretoken: csrf_token,
                    feed: $('#id_feed').val(),
                    url: $('#id_url').val(),
                    label: $('#id_label').val(),
                    is_active: is_active,
                    email: $('#id_email').val(),
                    notes: $('#id_notes').val(),
                    frequency: $('#id_frequency').val(),
                    day_of_week: $('#id_day_of_week').val(),
                    day_of_month: $('#id_day_of_month').val()
            },
            type: 'POST',
            url: '',
            success: function(data) {
                if (data == 'success') {
                    clearForm(form);
                    window.location.reload(true);
                } else {
                    form.replaceWith(data);
                    add_valid_label();
                    date_select();
                    reposition_errors();
                }
            }
        });
    }
}

function date_select() {
    // Only show the day of week/day of month field when appropriate
    if ($('#id_frequency').attr('value') == 'D') {
        $('label[for="id_day_of_month"]').hide();
        $('label[for="id_day_of_week"]').hide();
        $('#id_day_of_month').hide();
        $('#id_day_of_week').hide();
    } else if ($('#id_frequency').attr('value') == 'M') { 
        $('label[for="id_day_of_week"]').hide();
        $('#id_day_of_week').hide();
        $('label[for="id_day_of_month"]').css('display', 'inline');
        $('#id_day_of_month').css('display', 'inline');
    } else if ($('#id_frequency').attr('value') == 'W') {
        $('label[for="id_day_of_month"]').hide();
        $('#id_day_of_month').hide();
        $('label[for="id_day_of_week"]').css('display', 'inline');
        $('#id_day_of_week').css('display', 'inline');
    }

    $('#id_frequency').change(function() {
        if ($('#id_frequency').attr('value') == 'D') {
            $('label[for="id_day_of_month"]').hide();
            $('label[for="id_day_of_week"]').hide();
            $('#id_day_of_month').hide();
            $('#id_day_of_week').hide();
        } else if ($('#id_frequency').attr('value') == 'M') { 
            $('label[for="id_day_of_week"]').hide();
            $('#id_day_of_week').hide();
            $('label[for="id_day_of_month"]').css('display', 'inline');
            $('#id_day_of_month').css('display', 'inline');
        } else if ($('#id_frequency').attr('value') == 'W') {
            $('label[for="id_day_of_month"]').hide();
            $('#id_day_of_month').hide();
            $('label[for="id_day_of_week"]').css('display', 'inline');
            $('#id_day_of_week').css('display', 'inline');
        }
    });
}

function add_valid_label() {
    $('#id_url').after('<div id="validated_label" class="form-label pull-left">&nbsp;</div><div id="validated">&nbsp;</div>');
    $('#id_url').after('<div class="clear"></div>');
    $('#id_frequency').next('.clear').remove();
    $('#id_day_of_month').next('.clear').remove();
}

function reposition_errors() {
    $('label[for="id_label"]').replaceWith('&nbsp;');
    $('div.alert-message.block-message.error').each(function() {
        $(this).prev().after($($(this).children('[class!=errorlist]')));
        $(this).css('float', 'right');
    });
}
