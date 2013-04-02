$(document).ready(function() {
    check_digest_options();
    save_modal_form('id_', 'new_modal', 'new_search');
    save_modal_form('id_edit_', 'edit_modal', 'save_edit');
    resize_modal('#new_modal');
    add_valid_label('id_');
    disable_fields('id_', 'new_modal');
    validate_url('id_', 'new_modal');
    validate_url('id_edit_', 'edit_modal');
    add_refresh_btn('id_');

    $(window).resize(function() {
        resize_modal('#new_modal');
        resize_modal('#edit_modal');
    });

    $('#new_modal').on('hidden', function() {
        clearForm($('form#saved-search-form'));
        // Despite these two elements having null=True in the model,
        // having them actually be null causes errors
        $('#id_day_of_month, #id_day_of_week').val('1');
        $('#id_frequency').val('W');
        disable_fields('id_', 'new_modal');
        $('#id_url').blur();
        $('#id_validated').remove();
        add_errors('id_', '');
    });

    $('#edit_modal').on('hidden', function() {
        $('#edit_modal').children().remove();
    });

    $('td.view_search').click(function() {
        if ($(window).width() > 500) {
            var id = $(this).parent().attr('id');
            $('#search_'+id).modal();
        }
    });

    $('#new_btn').click(function(e) {
        e.preventDefault();
        $('#new_modal').modal();
    });

    $('a.edit').click(function(e) {
        e.preventDefault();
        get_edit($(this).attr('href'));
    });

});

function add_refresh_btn(prefix) {
    hashPrefix = '#' + prefix;
    $(hashPrefix+'url').parent().addClass('input-append');
    $(hashPrefix+'url').after('<span id="'+prefix+'refresh" class="btn add-on">refresh</span>');
}

function date_select(prefix) {
    // Only show the day of week/day of month field when appropriate
    var hashPrefix = '#' + prefix;

    $('label[for="'+prefix+'day_of_month"]').unwrap();
    $('label[for="'+prefix+'day_of_week"]').unwrap();
    show_dates();

    $(hashPrefix+'frequency').on('change', function() {
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
            $('label[for="'+prefix+'day_of_month"]').css('display', 'inline')
            $(hashPrefix+'day_of_week').hide();
            $(hashPrefix+'day_of_month').show();
        } else if ($(hashPrefix+'frequency').attr('value') == 'W') {
            $('label[for="'+prefix+'day_of_month"]').hide();
            $('label[for="'+prefix+'day_of_week"]').css('display', 'inline')
            $(hashPrefix+'day_of_month').hide();
            $(hashPrefix+'day_of_week').show();
        }
    }
}

function add_valid_label(prefix) {
    hashPrefix = '#' + prefix;
    $(hashPrefix+'url').after('<div id="'+prefix+'validated_label" class="form-label pull-left">&nbsp;</div>');
    $(hashPrefix+'validated_label').after('<div id="'+prefix+'validated">&nbsp;</div>');
    $(hashPrefix+'url').after('<div class="clear"></div>');
    $(hashPrefix+'frequency').next('.clear').remove();
    $(hashPrefix+'day_of_month').next('.clear').remove();
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

function disable_fields(prefix, modal) {
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
        $('label[for="'+prefix+'label"]').hide()
        $('label[for="'+prefix+'notes"]').hide();
        $('label[for="'+prefix+'day_of_week"]').hide();
        $('label[for="'+prefix+'day_of_month"]').hide();
        $('#'+modal+' .save').hide();
    }
}

// AJAX

/*
Retrieves compiled Edit Saved Search form

:id: ID of saved search to be edited
*/
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
            $('#edit_modal').append(data);
            add_valid_label(prefix);
            date_select(prefix);
            resize_modal('#edit_modal');
            disable_fields(prefix, 'edit_modal');
            $('#edit_modal').on('resize', function() {
                resize_modal('#edit_modal');
            });
            add_refresh_btn('id_edit_');
            $('#edit_modal').modal();
        }
    });
}

/*
Saves Saved Search forms

:prefix: id prefix used by the form
:modal: modal window that the form is nested inside
:action: action to undertake in views.py
*/
function save_modal_form(prefix, modal, action) {
    $('#'+modal).on('click', '#'+action, function(e) {
        e.preventDefault();
        save_form(prefix, modal, action);
    });

    function save_form(prefix, modal, action) {
        hashPrefix = '#' + prefix;
        var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var is_active = $(hashPrefix+'is_active').prop('checked')? 'True':'False';
        var form = $('#'+modal+' form');
        var id = form.find('a.save').attr('href');
        $.ajax({
            data: { action: action,
                    search_id: id,
                    csrfmiddlewaretoken: csrf_token,
                    feed: $(hashPrefix+'feed').val(),
                    url: $(hashPrefix+'url').val(),
                    label: $(hashPrefix+'label').val(),
                    is_active: is_active,
                    email: $(hashPrefix+'email').val(),
                    notes: $(hashPrefix+'notes').val(),
                    frequency: $(hashPrefix+'frequency').val(),
                    day_of_week: $(hashPrefix+'day_of_week').val(),
                    day_of_month: $(hashPrefix+'day_of_month').val()
            },
            type: 'POST',
            url: '',
            success: function(data) {
                if (data == 'success') {
                    clearForm(form);
                    window.location.reload(true);
                } else {
                    json = jQuery.parseJSON(data);
                }
            },
            complete: function(data) {
                var json;
                if (data == 'success') {
                    json = '';
                } else {
                    json = jQuery.parseJSON(data['responseText']);
                }
                add_errors(prefix, json);
            }
        });
    }
}

/*
Adds/removes errors to new search and edit search forms

:prefix: id prefix used by the form
:json: JSON string denoting which fields have errors
*/
function add_errors(prefix, json) {
    var hashPrefix = '#' + prefix;
    $('#saved-search-form [class*=label-important]').remove();
    if (json.indexOf('url') > -1) {
        $(hashPrefix+'refresh').after('<span class="label label-important">Required</span>');
    }
    if (json.indexOf('label') > -1) {
        $(hashPrefix+'label').after('<span class="label label-important">Required</span>');
    }
    if (json.indexOf('email') > -1) {
        $(hashPrefix+'email').after('<span class="label label-important">Required</span>');
    }
    if (json.indexOf('day_of_week') > -1 || json.indexOf('day_of_month') > -1) {
        $(hashPrefix+'day_of_week').after('<span class="label label-important">Required</span>');
    }
}

/*
Ensures url is a valid job rss feed

:prefix: id prefix used by the form
:modal: modal window that the form is nested inside
*/
function validate_url(prefix, modal) {
    // When user stops typing, an ajax request is sent to Django where it checks for
    // the validity of the URL. If it's valid, it informs the user and unblocks the
    // remaining fields.
    var timer;
    var pause_interval = 1000;
    var hashPrefix = '#' + prefix;

    // Known Firefox/Opera bug: this captures presses of the Esc key
    $('#'+modal).on('keypress cut paste input', hashPrefix+'url', function(){
        clearTimeout(timer);
        if ($(hashPrefix+'url').val()) {
            timer = setTimeout(function() {
                validate(prefix, modal);
            }, pause_interval);
        }
    });

    $('#'+modal).on('click', hashPrefix+'refresh', function() {
        validate(prefix, modal);
    });

    function validate(prefix, modal) {
        var hashPrefix = '#' + prefix;
        var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var form = $(hashPrefix+'url').parents('form');
        var url = $(hashPrefix+'url').val(); 
        validation_status('validating...', prefix)
        $.ajax({
            type: "POST",
            url: "",
            data: { csrfmiddlewaretoken: csrf_token,
                    action: "validate",
                    url: url},
            success: function(data) {
                var json = jQuery.parseJSON(data);
                if (json.url_status == 'valid') {
                    validation_status(json.url_status, prefix);
                    enable_fields(prefix, modal);
                    date_select(prefix);
                    if ($(hashPrefix+'label').val().length == 0) {
                        $(hashPrefix+'label').val(json.feed_title);
                    }
                    if ($(hashPrefix+'feed').val() != json.rss_url) {
                        $(hashPrefix+'feed').val(json.rss_url);
                    }
                }
                else {
                    validation_status(json.url_status, prefix);
                }
            }
        });

        function enable_fields(prefix, modal) {
            $(hashPrefix+'label').removeAttr("disabled");
            $(hashPrefix+'label').show();
            $(hashPrefix+'is_active').removeAttr("disabled");
            $(hashPrefix+'is_active').show();
            $(hashPrefix+'email').removeAttr("disabled");
            $(hashPrefix+'email').show();
            $(hashPrefix+'frequency').removeAttr("disabled");
            $(hashPrefix+'frequency').show();
            $(hashPrefix+'notes').removeAttr("disabled");
            $(hashPrefix+'notes').show();
            $(hashPrefix+'day_of_week').removeAttr("disabled");
            $(hashPrefix+'day_of_week').show();
            $(hashPrefix+'day_of_month').removeAttr("disabled");
            $(hashPrefix+'day_of_month').show();
            $('label[for="'+prefix+'frequency"]').show();
            $('label[for="'+prefix+'label"]').show();
            $('label[for="'+prefix+'email"]').show();
            $('label[for="'+prefix+'is_active"]').show();
            $('label[for="'+prefix+'notes"]').show();
            $('#'+modal+' .save').show();
        }

        function validation_status(status, prefix) {
            var hashPrefix = '#' + prefix;
            var label_text;

            if (status == 'valid') {
                label_text = 'label label-success';
            } else {
                label_text = 'label label-important';
            }
            if ($(hashPrefix+'validated').length) {
                $(hashPrefix+'validated').removeAttr('class');
                $(hashPrefix+'validated').addClass(label_text);
                $(hashPrefix+'validated').text(status);
            } else {
                $(hashPrefix+'validated_label').after('<div id="'+prefix+'validated" class="'+label_text+'">'+status+'</div>');
            }
        };
    }
}

/*
Checks and saves the Digest Options form
*/
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
