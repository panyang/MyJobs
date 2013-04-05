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
        add_errors('id_', 'new_modal', '');
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

    $('a.edit').click(function(e) {
        e.preventDefault();
        get_edit($(this).attr('href'));
    });

});
