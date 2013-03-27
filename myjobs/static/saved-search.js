$(document).ready(function() {
    $('#id_url').after('<div id="validated_label" class="form-label pull-left">&nbsp;</div><div id="validated">&nbsp;</div>');
    $('#id_url').after('<div class="clear"></div>');
    $('#id_frequency').next('.clear').remove();
    $('#id_day_of_month').next('.clear').remove();

    // Disable/hide fields until valid URL is entered
    if ($("#id_url").val().length == 0 ) {
        $('#id_label').attr("disabled", "disabled");
        $('#id_label').hide();
        $('#id_is_active').attr("disabled", "disabled");
        $('#id_is_active').hide();
        $('#id_email').attr("disabled", "disabled");
        $('#id_email').hide();
        $('#id_frequency').attr("disabled", "disabled");
        $('#id_frequency').hide();
        $('#id_notes').attr("disabled", "disabled");
        $('#id_notes').hide();
        $('#id_day_of_week').attr("disabled", "disabled");
        $('#id_day_of_week').hide();
        $('#id_day_of_month').attr("disabled", "disabled");
        $('#id_day_of_month').hide();
        $('label[for="id_frequency"]').hide();
        $('label[for="id_email"]').hide();
        $('label[for="id_is_active"]').hide();
        $('label[for="id_label"]').replaceWith('&nbsp;');
        $('label[for="id_notes"]').hide();
        $('#add_save').hide();
    }
    validate_url();
});
