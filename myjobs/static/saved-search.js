$(document).ready(function() { 
    date_select();
    $('label[for="id_label"]').hide();
    $('label[for="id_is_active"]').hide();
    $('label[for="id_email"]').hide();
    $('label[for="id_frequency"]').hide();
    $('label[for="id_notes"]').hide();
    $('label[for="id_day_of_week"]').hide();
    $('label[for="id_day_of_month"]').hide();
    $('#id_label').hide();
    $('#id_is_active').hide();
    $('#id_email').hide();
    $('#id_frequency').hide();
    $('#id_notes').hide();
    $('#id_day_of_week').hide();
    $('#id_day_of_month').hide();
    validate_url();
});

function validate_url() {
    var timer;
    var pause_interval = 1000;

    $('#id_url').keyup(function(){
        clearTimeout(timer);
        if ($('#id_url').val) {
            timer = setTimeout(validate, pause_interval);
        }
    });

    function validate () {
        var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var form = $('form');
        var url = form.find("#id_url").val();
        $.ajax({
            type: "POST",
            url: "",
            data: { csrfmiddlewaretoken: csrf_token,
                    action: "validate",
                    url: url},
            success: function(data) {
                var json = jQuery.parseJSON(data);
                if (json.url_status == 'valid') {
                    form.find("#id_url").after(' Validated!');
                    $('label[for="id_label"]').fadeIn();
                    $('label[for="id_is_active"]').fadeIn();
                    $('label[for="id_email"]').fadeIn();
                    $('label[for="id_frequency"]').fadeIn();
                    $('label[for="id_notes"]').fadeIn();
                    $('label[for="id_day_of_week"]').fadeIn();
                    $('label[for="id_day_of_month"]').fadeIn();
                    $('#id_label').fadeIn();
                    $('#id_is_active').fadeIn();
                    $('#id_email').fadeIn();
                    $('#id_frequency').fadeIn();
                    $('#id_notes').fadeIn();
                    $('#id_day_of_week').fadeIn();
                    $('#id_day_of_month').fadeIn();
                    form.find("#id_label").val(json.feed_title);
                    form.find("#id_feed").val(json.rss_url);
                }
                else {
                    form.find("#id_url").after(' Not valid');
                }
            }
        });
    }
};
function date_select() {
    if ($('#id_frequency').attr('value') == 'D') {
        $('label[for="id_day_of_month"]').hide();
        $('label[for="id_day_of_week"]').hide();
        $('#id_day_of_month').hide();
        $('#id_day_of_week').hide();
    } else if ($('#id_frequency').attr('value') == 'M') { 
        $('label[for="id_day_of_week"]').hide();
        $('#id_day_of_week').hide();
        $('label[for="id_day_of_month"]').show();
        $('#id_day_of_month').show();
    } else if ($('#id_frequency').attr('value') == 'W') {
        $('label[for="id_day_of_month"]').hide();
        $('#id_day_of_month').hide();
        $('label[for="id_day_of_week"]').show();
        $('#id_day_of_week').show();
    }

    $('#id_frequency').change(function() {
        if ($('#id_frequency').attr('value') == 'D') {
            $('label[for="id_day_of_month"]').hide();
            $('label[for="id_day_of_week"]').hide();
            $('#id_day_of_month').hide();
            $('#id_day_of_week').hide();
        } else if ($('#id_frequency').attr('value') == 'M') { 
            $('label[for="id_day_of_week"]').hide();
            $('#id_day_of_week').hide();
            $('label[for="id_day_of_month"]').show();
            $('#id_day_of_month').show();
        } else if ($('#id_frequency').attr('value') == 'W') {
            $('label[for="id_day_of_month"]').hide();
            $('#id_day_of_month').hide();
            $('label[for="id_day_of_week"]').show();
            $('#id_day_of_week').show();
        }
    });
};
