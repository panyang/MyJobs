function add_errors(that, data) {
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

function add_refresh_btn(that) {
    that.find('[id$="url"]').parent().addClass('input-append');
    that.find('[id$="url"]').after('<span class="btn add-on refresh"><i class="icon icon-refresh">');
}

function add_valid_label(that) {
    that.find('[id$="url"]').after('<div id="label_validated" class="span3 form-label pull-left id_label"><div class="form-label pull-left">&nbsp;</div>');
    that.find('[id$="label_validated"]').after('<div id="validated">&nbsp;</div>');
    that.find('[id$="url"]').after('<div class="clear"></div>');
}

function disable_fields(that) {
    // Disable/hide fields until valid URL is entered
    if (that.find('[id$="url"]').val() == '') {
        that.find('[id^="id_sort_by_"]').attr("disabled", "disabled");
        that.find('[id^="id_sort_by_"]').hide();
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
        that.find('label[for^="id_sort_by_"]').hide();
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

function enable_fields(that) {
    that.find('[id^="id_sort_by_"]').removeAttr("disabled");
    that.find('[id^="id_sort_by_"]').show();
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
    that.find('label[for^="id_sort_by_"]').show();
    that.find('label[for$="frequency"]').show();
    that.find('label[for$="label"]').show();
    that.find('label[for$="email"]').show();
    that.find('label[for$="is_active"]').show();
    that.find('label[for$="notes"]').show();
    that.find('.save').show();
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
