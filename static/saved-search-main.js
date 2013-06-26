$(function() {
    var SearchView = Backbone.View.extend({
        el: 'body',

        events: {
            'click [class$="edit"]': 'get_edit',
            'click [id$="_search"]': 'save_form',
            'click [class$="refresh"]': 'validate',
            'input input[id$="url"]': 'validate',
            'keypress input[id$="url"]': 'validate',
            'cut input[id$="url"]': 'validate',
            'paste input[id$="url"]': 'validate',
            'click [id$="digest_submit"]': 'check_digest_options',
            'click [class$="details"]': 'show_details',
            'click #delete': 'delete_search',
        },


        get_edit: function(e) {
            e.preventDefault();

            var that = $('#edit_modal');
            var id = $(e.target).attr('href');
            csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            $.ajax({
                data: { csrfmiddlewaretoken: csrf_token,
                        action: 'get_edit',
                        search_id: id },
                url: '/saved-search/edit',
                success: function(data) {
                    $('#edit_modal').append(data);
                    add_valid_label(that);
                    disable_fields(that);
                    enable_fields(that);
                    date_select(that);
                    add_refresh_btn(that);
                    $('#edit_modal').modal();
                }
            });
        },


        save_form: function(e, options) {
            e.preventDefault();

            var form = $(e.target).parents('#saved-search-form');
            var id = form.find('a.save').attr('href')
            var first_instance = 1;
            if ($('.table').length) {
                first_instance = 0;
            }
            
            var view_feed = $('#saved-search-listing-table').length;
            var render = '';
            if (view_feed) {
                render = 'False';
            } else {
                render = 'True';
            }

            data = form.serialize();
            data += '&search_id='+id;
            data += '&first_instance='+first_instance;
            data += '&render='+render;
            data = data.replace('=on','=True').replace('=off','=False');
            data = data.replace('undefined', 'None');
            $.ajax({
                data: data,
                type: 'POST',
                url: '/saved-search/save',
                success: function(response) {
                    if (response == '') {
                        window.location = window.location;
                    } else if (response.indexOf('<td') > -1) {
                        if (first_instance) {
                            $('#saved-search-list p').remove();
                            $('#saved-search-list').prepend(response);
                        } else {
                            $('#saved-search-'+id).remove();
                            $('tbody').append(response);
                        }
                        $('[id$="modal"]').modal('hide');
                        clearForm(form);
                        response = '';
                    }
                    add_errors(form, response);
                }
            });
        },


        validate: function(e) {
            var that = $(e.target).parents('#saved-search-form');
            if (e.target == that.find('[id$="url"]').get(0)) {
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
                var url = that.find('[id$="url"]').val(); 
                validation_status('validating...', that)
                $.ajax({
                    type: "POST",
                    url: "/saved-search/validate-url",
                    data: { csrfmiddlewaretoken: csrf_token,
                            action: "validate",
                            url: url},
                    success: function(data) {
                        var json = jQuery.parseJSON(data);
                        if (json.url_status == 'valid') {
                            validation_status(json.url_status, that);
                            enable_fields(that);
                            date_select(that);
                            if (that.find('[id$="label"]').val().length == 0) {
                                that.find('[id$="label"]').val(json.feed_title);
                            }
                            if (that.find('[id$="feed"]').val() != json.rss_url) {
                                that.find('[id$="feed"]').val(json.rss_url);
                            }
                        
                        marginTop = (($('#new_modal').height())/2) *-1 + "px";
                        $('#new_modal').css({'margin-top': marginTop});
                        }
                        else {
                            validation_status(json.url_status, that);
                        }
                    }
                });
                function validation_status(status, that) {
                    var label_text;

                    if (status == 'valid') {
                        label_text = 'label label-success';
                    } else {
                        label_text = 'label label-important';
                    }
                    if (that.find('#validated').length) {
                        that.find('#validated').removeAttr('class');
                        that.find('#validated').addClass(label_text);
                        that.find('#validated').text(status);
                    } else {
                        that.find('#label_validated').after('<div id="'+
                                                              'validated" class="'+
                                                              label_text+'">'+status+
                                                              '</div>');
                    }
                }
            }
        },


        check_digest_options: function(e) {
            // When the user interacts with any fields in the Digest Options form,
            // an ajax request checks that the form is valid and saves the changes
            e.preventDefault();
            var that = $(e.target).parents('#digest-option');

            save_digest_form();

            function save_digest_form() {
                var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

                $.ajax({
                    data: { csrfmiddlewaretoken: csrf_token, action: 'save',
                            is_active: $('#id_digest_active').prop('checked')?
                                                                   'True':'False',
                            email: $('#id_digest_email').val(),
                            send_if_none: $('#id_send_if_none').prop('checked')?
                                                                     'True':'False' },
                    type: 'POST',
                    url: 'save-digest',
                    success: function(data) {
                        if (data == 'success') {
                            form_status('Saved!');
                        } else {
                            form_status('Something went wrong');
                        }
                    }
                });

                function form_status(status) {
                    var delay = 5000;
                    var timer;
                    clearTimeout(timer);
                    that.find('#saved').addClass('label label-info');
                    $('#saved').text(status);
                    // Fade in 600ms, wait 5s, fade out 600ms
                    $('#saved').fadeIn('slow');
                    timer = setTimeout('$("#saved").fadeOut("slow")', delay);
                }
            }
        },


        show_details: function(e) {
            e.preventDefault();
            id = $(e.target).attr('href')
            $('[id^="search_'+id+'"]').modal();
        },


        delete_search: function(e) {
            e.preventDefault();

            id = $(e.target).attr('href');

            $.ajax({
                url: '/saved-search/delete/'+id,
                success: function() {
                    $('#saved-search-'+id).remove();
                    if ($('tr[id^="saved-search-"]').length == 0) {
                        $('table').remove()
                        $('#saved-search-list').prepend(
                            '<p>No Saved Searches!</p>');
                    }
                    $('[id$="modal"]').modal('hide');
                }
            });
        },
    });

    var Search = new SearchView;
});


function enable_fields(that) {
    that.find('[id$="label"]').removeAttr("disabled");
    that.find('[id$="label"]').show();
    that.find('[id$="is_active"]').removeAttr("disabled");
    that.find('[id$="is_active"]').show();
    that.find('[id$="email"]').removeAttr("disabled");
    that.find('[id$="email"]').show();
    that.find('[id$="frequency"]').removeAttr("disabled");
    that.find('[id$="frequency"]').show();
    that.find('[id$="notes"]').removeAttr("disabled");
    that.find('[id$="notes"]').show();
    that.find('[id$="day_of_week"]').removeAttr("disabled");
    that.find('[id$="day_of_week"]').show();
    that.find('[id$="day_of_month"]').removeAttr("disabled");
    that.find('[id$="day_of_month"]').show();
    that.find('label[for$="frequency"]').show();
    that.find('label[for$="label"]').show();
    that.find('label[for$="email"]').show();
    that.find('label[for$="is_active"]').show();
    that.find('label[for$="notes"]').show();
    that.find('.save').show();
}

function add_refresh_btn(that) {
    that.find('[id$="url"]').parent().addClass('input-append');
    that.find('[id$="url"]').after('<span class="btn add-on refresh"><i class="icon icon-refresh">');
}

function date_select(that) {
    show_dates();

    that.find('[id$="frequency"]').on('change', function() {
        show_dates();
    });

    function show_dates() {
        if (that.find('[id$="frequency"]').attr('value') == 'D') {
            that.find('label[for$="day_of_month"]').hide();
            that.find('label[for$="day_of_week"]').hide();
            that.find('[id$="day_of_month"]').hide();
            that.find('[id$="day_of_week"]').hide();
        } else if (that.find('[id$="frequency"]').attr('value') == 'M') { 
            that.find('label[for$="day_of_week"]').hide();
            that.find('label[for$="day_of_month"]').show();
            that.find('[id$="day_of_week"]').hide();
            that.find('[id$="day_of_month"]').show();
        } else if (that.find('[id$="frequency"]').attr('value') == 'W') {
            that.find('label[for$="day_of_month"]').hide();
            that.find('label[for$="day_of_week"]').show();
            that.find('[id$="day_of_month"]').hide();
            that.find('[id$="day_of_week"]').show();
        }
    }
}

function add_valid_label(that) {
    that.find('[id$="url"]').after('<div id="label_validated" class="span3 form-label pull-left id_label"><div class="form-label pull-left">&nbsp;</div>');
    that.find('[id$="label_validated"]').after('<div id="validated">&nbsp;</div>');
    that.find('[id$="url"]').after('<div class="clear"></div>');
}

function disable_fields(that) {
    // Disable/hide fields until valid URL is entered
    if (that.find('[id$="url"]').val() == '') {
        that.find('[id$="label"]').attr("disabled", "disabled");
        that.find('[id$="label"]').hide();
        that.find('[id$="is_active"]').attr("disabled", "disabled");
        that.find('[id$="is_active"]').hide();
        that.find('[id$="email"]').attr("disabled", "disabled");
        that.find('[id$="email"]').hide();
        that.find('[id$="frequency"]').attr("disabled", "disabled");
        that.find('[id$="frequency"]').hide();
        that.find('[id$="notes"]').attr("disabled", "disabled");
        that.find('[id$="notes"]').hide();
        that.find('[id$="day_of_week"]').attr("disabled", "disabled");
        that.find('[id$="day_of_week"]').hide();
        that.find('[id$="day_of_month"]').attr("disabled", "disabled");
        that.find('[id$="day_of_month"]').hide();
        that.find('label[for$="frequency"]').hide();
        that.find('label[for$="email"]').hide();
        that.find('label[for$="is_active"]').hide();
        that.find('label[for$="label"]').hide()
        that.find('label[for$="notes"]').hide();
        that.find('label[for$="day_of_week"]').hide();
        that.find('label[for$="day_of_month"]').hide();
        that.find('.save').hide();
    }
}

function add_errors(that, data) {
    console.log(data)
    // remove color from labels of current errors
    $('[class*=required]').prev().children().css('color', '#000');

    // remove current errors
    $('[class*=required]').children().unwrap();

    errors = jQuery.parseJSON(data)
    for (var key in errors) {
        if (key == 'day_of_week' || key == 'day_of_month') {
            that.find('label[for$="frequency"]').parent().next().wrap('<span class="required" />');
            that.find('label[for$="frequency"]').css('color', '#900');
            that.find('label[for$="'+key+'"]').parent().next().wrap('<span class="required" />');
        } else {
            console.log(that.find('label[for$="'+key+'"]').parent().next())
            that.find('label[for$="'+key+'"]').parent().next().wrap('<span class="required" />');
            console.log(that.find('label[for$="'+key+'"]').parent().next())
            that.find('label[for$="'+key+'"]').parent().next().children().attr("placeholder","Required Field");
            that.find('label[for$="'+key+'"]').css('color', '#900');
        }
    }
}
