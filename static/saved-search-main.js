$(document).ready(function() {
    check_digest_options();
    save_new_form();
    resize_modal('#new_modal');
    add_valid_label('id_');
    disable_fields('id_');
    validate_url();

    $(window).resize(function() {
        resize_modal('#new_modal');
        resize_modal('#edit_modal');
    });

    $('#new_modal').on('hidden', function() {
        clearForm($('form#saved-search-form'));
        disable_fields();
        $('.alert-message.block-message.error').remove();
        $('#id_url').blur();
        $('#id_validated').replaceWith('&nbsp;');
    });

    $('#edit_modal').live('hidden', function() {
        $('#edit_modal').remove();
    });

    $('td.view_search').click(function() {
        var id = $(this).parent().attr('id');
        $('#search_'+id).modal();
        /*if (is_mobile() && typeof(href) != 'undefined') {
            window.location = href;
        }*/
    });

    $('#new_btn').click(function(e) {
        e.preventDefault();
        $('#new_modal').modal();
    });

    $('a.edit').click(function(e) {
        e.preventDefault();
        get_edit($(this).attr('href'));
        if ($(this).parent().hasClass('modal-footer')) {
            $(this).parents('.modal.hide.fade').modal('hide');
        }
    });

});

function get_edit(id) {
    var prefix = 'id_edit_';
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax({
        data: { csrfmiddlewaretoken: csrf_token,
                action: 'get_edit',
                search_id: id },
        type: 'POST',
        url: '',
        success: function(data) {
            $('#new_modal').after(data);
            add_valid_label(prefix);
            date_select(prefix);
            reposition_errors(prefix);
            resize_modal('#edit_modal');
            disable_fields('id_edit_');
            $('#edit_modal').live('resize', function() {
                resize_modal('#edit_modal');
            });
            $('#edit_modal').modal();
        }
    });
}

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
                    date_select(prefix);
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
            if ($("#id_validated").length) {
                $('#id_validated').removeAttr('class');
                $('#id_validated').addClass(label_text);
                $("#id_validated").text(status);
            } else {
                form.find("#id_validated_label").after(' <div id="id_validated" class="'+label_text+'">'+status+'</div>');
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
        var prefix = 'id_'
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
                    add_valid_label(prefix);
                    date_select(prefix);
                    reposition_errors(prefix);
                }
            }
        });
    }
}

function date_select(prefix) {
    // Only show the day of week/day of month field when appropriate
    var hashPrefix = '#' + prefix;

    show_dates();

    $(hashPrefix+'frequency').change(function() {
        show_dates();
    });

    function show_dates() {
        if ($(hashPrefix+'frequency').attr('value') == 'D') {
            $('label[for="'+prefix+'day_of_month"]').hide();
            $('label[for="'+prefix+'day_of_week"]').hide();
            $(hashPrefix+'day_of_month').hide();
            $(hashPrefix+'day_of_week').hide();
        } else if ($(hashPrefix+'frequency').attr('value') == 'M') { 
            $('label[for="'+prefix+'day_of_week"]').hide();
            $(hashPrefix+'day_of_week').hide();
            $('label[for="'+prefix+'day_of_month"]').css('display', 'inline');
            $(hashPrefix+'day_of_month').css('display', 'inline');
        } else if ($(hashPrefix+'frequency').attr('value') == 'W') {
            $('label[for="'+prefix+'day_of_month"]').hide();
            $(hashPrefix+'day_of_month').hide();
            $('label[for="'+prefix+'day_of_week"]').css('display', 'inline');
            $(hashPrefix+'day_of_week').css('display', 'inline');
        }
    }
}

function add_valid_label(prefix) {
    $(prefix+'url').after('<div id="'+prefix+'validated_label" class="form-label pull-left">&nbsp;</div><div id="'+prefix+'validated">&nbsp;</div>');
    $(prefix+'url').after('<div class="clear"></div>');
    $(prefix+'frequency').next('.clear').remove();
    $(prefix+'day_of_month').next('.clear').remove();
}

function reposition_errors(prefix) {
    $('label[for="'+prefix+'label"]').replaceWith('&nbsp;');
    $('div.alert-message.block-message.error').each(function() {
        $(this).prev().after($($(this).children('[class!=errorlist]')));
        $(this).css('float', 'right');
    });
}

function resize_modal(modal) {
    var max_height, margin_top, width, margin_left;
    max_height = $(window).height();
    width = $(window).width();
    if (!is_mobile()) {
        max_height = max_height * 0.8;
        width = width * 0.6;
    }
    margin_top = -(max_height/2);
    margin_left = -(width/2);
    $(modal).css({
        'max-height': max_height.toFixed(0) + 'px',
        'margin-top': margin_top.toFixed(0) + 'px',
        'width': width.toFixed(0) + 'px',
        'margin-left': margin_left.toFixed(0) + 'px',
    });
}

function is_mobile() {
    return $(window).width() <= 500;
}

function disable_fields(prefix) {
    // Disable/hide fields until valid URL is entered
    hashPrefix = '#' + prefix;
    if ($(hashPrefix+'url').val().length == 0 ) {
        $(hashPrefix+'label').attr("disabled", "disabled");
        $(hashPrefix+'label').hide();
        $(hashPrefix+'is_active').attr("disabled", "disabled");
        $(hashPrefix+'is_active').hide();
        $(hashPrefix+'email').attr("disabled", "disabled");
        $(hashPrefix+'email').hide();
        $(hashPrefix+'frequency').attr("disabled", "disabled");
        $(hashPrefix+'frequency').hide();
        $(hashPrefix+'notes').attr("disabled", "disabled");
        $(hashPrefix+'notes').hide();
        $(hashPrefix+'day_of_week').attr("disabled", "disabled");
        $(hashPrefix+'day_of_week').hide();
        $(hashPrefix+'day_of_month').attr("disabled", "disabled");
        $(hashPrefix+'day_of_month').hide();
        $('label[for="'+prefix+'frequency"]').hide();
        $('label[for="'+prefix+'email"]').hide();
        $('label[for="'+prefix+'is_active"]').hide();
        $('label[for="'+prefix+'label"]').replaceWith('&nbsp;');
        $('label[for="'+prefix+'notes"]').hide();
        $('#add_save').hide();
    }
}
