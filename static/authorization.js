/*
The login button on the authorization page sends an AJAX POST request when
clicked. This ensures that the information is correct. If the information is
correct, it redirects to the provided url. If not, it adds errors to the form.
*/
$(document).on('click', 'button#auth-login', function(e) {
    e.preventDefault();
    var form = $('#auth-form');
    var action = form.find('button').attr('value')
    var url = form.attr('action');
    form = form.serialize() + '&action=' + action;
    $.ajax({
        type: "POST",
        url: url,
        data: form,
        global: false,
        success: function(data) {
            var json = jQuery.parseJSON(data);
            // Check to see if json.url is present. If so, redirect to it.
            if (Boolean(json.url)){
                window.location = json.url;
            }else{
                // Remove all required field changes, if any
                removeRequiredChanges();

                // For every error passed by json, run jsonError function
                for (var index in json.errors) {
                    jsonErrors(index, json.errors);
                }
            }
        }
    });
});