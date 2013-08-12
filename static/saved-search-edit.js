$(function() {
    var EditSearchView = Backbone.View.extend({
        el: 'body',

        initialize: function() {
            this.once('renderEvent', function() {
                disable_fields();
                add_valid_label();
                add_refresh_btn();
            });
        },


        render: function() {
            this.trigger('renderEvent');
        },


        events: {
            'click [id$="_search"]': 'save_form',
            'click [class$="refresh"]': 'validate',
            'input input[id$="url"]': 'validate',
            'keypress input[id$="url"]': 'validate',
            'cut input[id$="url"]': 'validate',
            'paste input[id$="url"]': 'validate',
        },


        save_form: function(e, options) {
            e.preventDefault();

            var form = $('#saved-search-form');

            data = form.serialize();
            data = data.replace('=on','=True').replace('=off','=False');
            data = data.replace('undefined', 'None');
            $.ajax({
                data: data,
                type: 'POST',
                url: '/'+user_email+'/saved-search/save/',
                success: function(data) {
                    console.log(data)
                    if (data == '') {
                        window.location = '/'+user_email+'/saved-search/';
                    } else {
                        add_errors(data);
                    }
                }
            });
        },


        validate: function(e) {
            if (e.target == $('[id$="url"]').get(0)) {
                if (this.timer) {
                    clearTimeout(this.timer);
                }
                var pause_interval = 1000;
                this.timer = setTimeout(function() {
                    do_validate();
                }, pause_interval);
            } else {
                do_validate();
            }

            function do_validate() {
                var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
                var url = $('[id$="url"]').val(); 
                validation_status('validating...')
                $.ajax({
                    type: "POST",
                    url: "/"+user_email+"/saved-search/validate-url/",
                    data: { csrfmiddlewaretoken: csrf_token,
                            action: "validate",
                            url: url},
                    success: function(data) {
                        var json = jQuery.parseJSON(data);
                        if (json.url_status == 'valid') {
                            validation_status(json.url_status);
                            if ($('[id$="label"]').val().length == 0) {
                                $('[id$="label"]').val(json.feed_title);
                            }
                            if ($('[id$="feed"]').val() != json.rss_url) {
                                $('[id$="feed"]').val(json.rss_url);
                            }
                            enable_fields();
                            date_select();
                        }
                        else {
                            validation_status(json.url_status);
                        }
                    }
                });
                function validation_status(status) {
                    var label_text;

                    if (status == 'valid') {
                        label_text = 'label label-success';
                    } else {
                        label_text = 'label label-important';
                    }
                    if ($('#validated').length) {
                        $('#validated').removeAttr('class');
                        $('#validated').addClass(label_text);
                        $('#validated').text(status);
                    } else {
                        $('#label_validated').after('<div id="'+
                                                    'validated" class="'+
                                                    label_text+'">'+status+
                                                    '</div>');
                    }
                }
            }
        },
    });

    var EditSearch = new EditSearchView;
    EditSearch.render();
});

function add_errors(data) {
    // remove color from labels of current errors
    $('[class*=required]').prev().children().css('color', '#000');

    // remove current errors
    $('[class*=required]').children().unwrap();

    errors = jQuery.parseJSON(data)
    for (var key in errors) {
        if (key == 'day_of_week' || key == 'day_of_month') {
            $('label[for$="frequency"]').parent().next().wrap('<span class="required" />');
            $('label[for$="frequency"]').css('color', '#900');
            $('label[for$="'+key+'"]').parent().next().wrap('<span class="required" />');
        } else {
            $('label[for$="'+key+'"]').parent().next().wrap('<span class="required" />');
            $('label[for$="'+key+'"]').parent().next().children().attr("placeholder","Required Field");
            $('label[for$="'+key+'"]').css('color', '#900');
        }
    }
}

function add_refresh_btn() {
    $('[id$="url"]').parent().addClass('input-append');
    $('[id$="url"]').after('<span class="btn add-on refresh"><i class="icon icon-refresh">');
}

function add_valid_label() {
    $('[id$="url"]').after('<div id="label_validated" class="span3 form-label pull-left id_label"><div class="form-label pull-left">&nbsp;</div>');
    $('[id$="label_validated"]').after('<div id="validated">&nbsp;</div>');
    $('[id$="url"]').after('<div class="clear"></div>');
}

function disable_fields() {
    // Disable/hide fields until valid URL is entered
    if ($('[id$="url"]').val() == '') {
        $('[id^="id_edit_sort_by_"]').hide();
        $('label[for^="id_edit_sort_by_"]').hide();
        $('[id$="label"]').hide();
        $('label[for$="label"]').hide()
        $('[id$="is_active"]').hide();
        $('label[for$="is_active"]').hide();
        $('[id$="email"]').hide();
        $('label[for$="email"]').hide();
        $('[id$="frequency"]').hide();
        $('label[for$="frequency"]').hide();
        $('[id$="notes"]').hide();
        $('label[for$="notes"]').hide();
        $('[id$="day_of_week"]').hide();
        $('[id$="day_of_month"]').hide();
        $('label[for$="day_of_week"]').hide();
        $('label[for$="day_of_month"]').hide();
        $('.save').hide();
    } else {
        enable_fields();
        date_select();
    }
}

function enable_fields() {
    $('[id^="id_edit_sort_by_"]').show();
    $('label[for^="id_edit_sort_by_"]').show();
    $('[id$="label"]').show();
    $('label[for$="label"]').show();
    $('[id$="is_active"]').show();
    $('label[for$="is_active"]').show();
    $('[id$="email"]').show();
    $('label[for$="email"]').show();
    $('[id$="frequency"]').show();
    $('label[for$="frequency"]').show();
    $('[id$="notes"]').show();
    $('label[for$="notes"]').show();
    $('[id$="day_of_week"]').show();
    $('[id$="day_of_month"]').show();
    $('label[for$="day_of_week"]').show();
    $('label[for$="day_of_month"]').show();
    $('.save').show();
}

function date_select() {
    show_dates();

    $('[id$="frequency"]').on('change', function() {
        show_dates();
    });

    function show_dates() {
        if ($('[id$="frequency"]').attr('value') == 'D') {
            $('label[for$="day_of_month"]').hide();
            $('label[for$="day_of_week"]').hide();
            $('[id$="day_of_month"]').hide();
            $('[id$="day_of_week"]').hide();
        } else if ($('[id$="frequency"]').attr('value') == 'M') { 
            $('label[for$="day_of_week"]').hide();
            $('label[for$="day_of_month"]').show();
            $('[id$="day_of_week"]').hide();
            $('[id$="day_of_month"]').show();
        } else if ($('[id$="frequency"]').attr('value') == 'W') {
            $('label[for$="day_of_month"]').hide();
            $('label[for$="day_of_week"]').show();
            $('[id$="day_of_month"]').hide();
            $('[id$="day_of_week"]').show();
        }
    }
}
