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
                            frequency: $('#id_frequency').val(),
                            day_of_week: $('#id_day_of_week').val(),
                            day_of_month: $('#id_day_of_month').val(),
                            send_if_none: $('#id_send_if_none').prop('checked')?
                                                                     'True':'False' },
                    type: 'POST',
                    url: 'save-digest/',
                    success: function(data) {
                        if (data == '') {
                            form_status('Saved!');
                        } else {
                            form_status('Something went wrong');
                        }
                        add_errors(data);
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

    date_select();

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
            $('label[for$="'+key+'"]').css('color', '#900');
        } else {
            $('label[for$="'+key+'"]').parent().next().wrap('<span class="required" />');
            $('label[for$="'+key+'"]').parent().next().children().attr("placeholder","Required Field");
            $('label[for$="'+key+'"]').css('color', '#900');
        }
    }
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
