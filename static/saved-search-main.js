$(function() {
    var SearchView = Backbone.View.extend({
        el: 'body',

        events: {
            'click [id="digest_submit"]': 'check_digest_options',
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
                    url: 'save-digest/',
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
    });

    var Search = new SearchView;


    /*
    Targets event fired when "Search Name" column is clicked
    */
    $('.view_search').click(function(e) {
        // Only redirect when at mobile resolution (<= 500px)
        if ($(window).width() <= 500) {
            // id is formatted saved-search-[id]
            var id = $(e.target).closest('tr').attr('id').split('-')[2];
            window.location += 'feed?id=' + id;
        }
    });
});
