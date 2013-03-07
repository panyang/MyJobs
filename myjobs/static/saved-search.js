$(document).ready(function() {
    // Disable fields until valid URL is entered
    if ($("#id_url").val().length == 0 ) {
        $('#id_label').attr("disabled", "disabled");
        $('#id_is_active').attr("disabled", "disabled");
        $('#id_email').attr("disabled", "disabled");
        $('#id_frequency').attr("disabled", "disabled");
        $('#id_notes').attr("disabled", "disabled");
        $('#id_day_of_week').attr("disabled", "disabled");
    }
    date_select();
    validate_url();
});
