$(document).ready(function() {
    add_valid_label($('#new_modal'));
    disable_fields($('#new_modal'));
    add_refresh_btn($('#new_modal'));

    $('#new_modal').on('hidden', function() {
        clearForm($('form#saved-search-form'));
        // Despite these two elements having null=True in the model,
        // having them actually be null causes errors
        $('#id_day_of_month, #id_day_of_week').val('1');
        $('#id_frequency').val('W');
        disable_fields($('#new_modal'));
        $('#id_url').blur();
        $('#validated').remove();
        add_errors($('#new_modal'), '');
    });

    $('#edit_modal').on('hidden', function() {
        $('#edit_modal').children().remove();
    });

    $('a.btn.mobile_hide.details').click(function(e) {
        e.preventDefault();
        if ($(window).width() > 500) {
            var id = $(this).attr('href');
            $('#search_'+id).modal();
        }
    });

    $('#new_btn').click(function(e) {
        e.preventDefault();
        $('#new_modal').modal();
    });

    /*
    Targets event fired when "Search Name" column is clicked
    */
    $('.view_search').click(function(e) {
        // Only redirect when at mobile resolution (<= 500px)
        if ($(window).width() <= 500) {
            // id is formatted saved-search-[id]
            var id = $(e.target).parent().attr('id').split('-')[2];
            window.location = id;
        }
    });
});
