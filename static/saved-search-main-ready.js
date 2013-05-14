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
});
