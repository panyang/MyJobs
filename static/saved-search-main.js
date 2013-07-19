$(function() {
    var SearchView = Backbone.View.extend({
        el: 'body',

        events: {
            'click [id$="_search"]': 'save_form',
            'click [class$="refresh"]': 'validate',
            'input input[id$="url"]': 'validate',
            'keypress input[id$="url"]': 'validate',
            'cut input[id$="url"]': 'validate',
            'paste input[id$="url"]': 'validate',
            'click [id$="digest_submit"]': 'check_digest_options',
        },


        save_form: function(e, options) {
            e.preventDefault();

            var form = $(e.target).parents('form');
            
            data = form.serialize();
            data = data.replace('=on','=True').replace('=off','=False');
            data = data.replace('undefined', 'None');
            $.ajax({
                data: data,
                type: 'POST',
                url: '/saved-search/save/',
                success: function(data) {
                    if (data == '') {
                        window.location = '/saved-search/';
                    } else {
                        add_errors(form, data);
                    }
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
                    url: "/saved-search/validate-url/",
                    data: { csrfmiddlewaretoken: csrf_token,
                            action: "validate",
                            url: url},
                    success: function(data) {
                        var json = jQuery.parseJSON(data);
                        if (json.url_status == 'valid') {
                            validation_status(json.url_status, that);
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
    });

    var Search = new SearchView;
});
