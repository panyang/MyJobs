$(document).ready(function() {
    var timer;
    var pause_interval = 100;

    $('#id_url').keyup(function(){
        clearTimeout(timer);
        if ($('#id_url').val) {
            timer = setTimeout(validate_url, pause_interval);
        }
    });

    function validate_url (csrf_token) {
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
                    form.find("#id_label").val(json.feed_title);
                    form.find("#id_feed").val(json.rss_url);
                }
                else {
                    form.find("#id_url").after(' Not valid');
                }
            }
        });
    }
});
