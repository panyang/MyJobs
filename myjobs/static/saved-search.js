$(document).ready(function() {
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

    $('#id_email').autocomplete(emails);

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
        validation_status('Validating...')
        $.ajax({
            type: "POST",
            url: "",
            data: { csrfmiddlewaretoken: csrf_token,
                    action: "validate",
                    url: url},
            success: function(data) {
                var json = jQuery.parseJSON(data);
                if (json.url_status == 'valid') {
                    validation_status('Validated!');
                    $('#id_label').removeAttr("disabled");
                    $('#id_is_active').removeAttr("disabled");
                    $('#id_email').removeAttr("disabled");
                    $('#id_frequency').removeAttr("disabled");
                    $('#id_notes').removeAttr("disabled");
                    $('#id_day_of_week').removeAttr("disabled");
                    form.find("#id_label").val(json.feed_title);
                    form.find("#id_feed").val(json.rss_url);
                }
                else {
                    validation_status('Not Valid');
                }
            }
        });

        function validation_status(status) {
            if ($("#validated").length) {
                $("#validated").text(status);
            } else {
                form.find("#id_url").after(' <div id="validated">'+status+'</div>');
            }
        };
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
