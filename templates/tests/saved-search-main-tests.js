var ajax, disable;
module("saved-search-main.js AJAX Tests", { setup: function() {
    // backup the methods to be mocked
    ajax = $.ajax;
    disable = disable_fields;
    $('#qunit-fixture').append($('<input />',
                               { name: 'csrfmiddlewaretoken',
                                 value: 'foo' }));
}, teardown: function() {
    // return mocked methods to their original values
    $.ajax = ajax;
    disable_fields = disable;
}});
test("get_edit", function() {
    $('#qunit-fixture').append($('<div />',
                                 { id: 'container',
                                   'class': 'row' }));
    $('#container').append($('<div />', { id: 'edit_modal' }));
    $('#container').append($('<a />',
                               { 'class': 'edit',
                                 href: '1' }));
    $.ajax = function(params) {
        if (params.url == 'edit' && params.data.csrfmiddlewaretoken == 'foo') {
            params.success('query successful');
        }
    };
    disable_fields = function(param1, param2) {
    };
    $('.edit').trigger('click');
    $('#edit_modal').modal('hide');
    equal($('#edit_modal').html(), 'query successful', "AJAX response should"+
                                                       " be appended to #edit"+
                                                       "_modal");
});
test("save_form", function() {
    $('#qunit-fixture').append($('<div />',
                               { id: 'save_test',
                                 'class': 'row' }));
    $('#save_test').append($('<form />',
                               { id: 'saved-search-form' }));
    $('#saved-search-form').append($('<input />',
                               { id: 'id_url', type: 'text' }));
    $('#saved-search-form').append($('<span />',
                               { id: 'id_refresh' }));
    $('#saved-search-form').append($('<input />',
                               { id: 'id_is_active', type: 'checkbox' }));
    $('#saved-search-form').append($('<a />',
                               { id: 'new_search' }));
    $('#id_is_active').checked = true;
    $.ajax = function(params) {
        params.complete = function() {};
        if (params.data.url == 'jobs.jobs/jobs') {
            params.success('success');
        } else {
            params.success(['url']);
        }
    };
    function success_callback() {};
    equal($('#saved-search-form').children().length, 4, "Form should have only"+
                                                        " three children");
    $('#new_search').trigger('click', { success_callback: success_callback });
    equal($('#saved-search-form').children().length, 5, "Form should have an"+
                                                        " error label added");

    $('#id_url').val('jobs.jobs/jobs');
    $('#new_search').trigger('click', { success_callback: success_callback });
    equal($('#id_url').val(), '', "#id_url should be cleared after submitting"+
                                  " a valid form");
    equal($('#id_is_active').checked, undefined, "#id_is_active should be"+
                                                 " cleared");
    equal($('#saved-search-form').children().length, 4, "Error label should be"+
                                                        " removed");
});
test("validate", function() {
    $('#qunit-fixture').append($('<div />',
                               { id: 'container',
                                 'class': 'row' }));
    $('#container').append($('<form />',
                               { id: 'saved-search-form' }));
    $('#saved-search-form').append($('<input />',
                               { id: 'id_url', type: 'text' }));
    $('#saved-search-form').append($('<div />',
                               { 'class': 'refresh' }));
    $('#saved-search-form').append($('<input />',
                               { id: 'id_feed', type: 'text' }));
    $('#saved-search-form').append($('<input />',
                               { id: 'id_label', type: 'text' }));
    $('#saved-search-form').append($('<div />', { id: 'validated' }));
    $.ajax = function(params) {
        if (params.data.url == 'jobs.jobs/jobs') {
            params.success('{"url_status":"valid","feed_title":"foo","rss_url"'+
                           ':"bar"}');
        } else {
            params.success('{"url_status":"not valid"}');
        }
    }
    $('.refresh').click();
    equal($('#validated').text(), 'not valid', "Running validate with no feed"+
                                             " url returns 'not valid'");
    equal($('#id_feed').text(), '', "With no url, #id_feed should be empty");
    equal($('#id_label').text(), '', "With no url, #id_label should be empty");

    $('#id_url').val('google.com');
    $('.refresh').click();
    equal($('#validated').text(), 'not valid', "Running validate with an"+
                                               " invalid feed url returns"+
                                               " 'not valid'");
    equal($('#id_feed').text(), '', "With an invalid url, #id_feed should be"+
                                    " empty");
    equal($('#id_label').text(), '', "With an invalid url, #id_label should be"+
                                     " empty");

    $('#id_url').val('jobs.jobs/jobs');
    $('.refresh').click();
    equal($('#validated').text(), 'valid', "Running validate with a valid"+
                                           " url returns 'valid'");
    equal($('#id_feed').val(), 'bar', "With a valid url, #id_feed should get"+
                                      " set");
    equal($('#id_label').val(), 'foo', "With a valid url, #id_label should"+
                                       " get set");
});
test("save_digest_form", function() {
    $('#qunit-fixture').append($('<div />', { id: 'digest-option' }));
    $('#digest-option').append($('<input />', { id: 'id_digest_active',
                                                type: 'checkbox' }));
    $('#digest-option').append($('<input />', { id: 'id_digest_email',
                                                type: 'text' }));
    $('#digest-option').append($('<input />', { id: 'id_send_if_none',
                                                type: 'checkbox' }));
    $('#digest-option').append($('<span />', { id: 'saved' }));
    $('#digest-option').append($('<div />', { id: 'digest_submit' }));
    $.ajax = function(params) {
        if (params.data.is_active == 'True') {
            if (params.data.email == '') {
                params.success('fail');
            } else {
                params.success('success');
            }
        } else {
            params.success('success');
        }
    }
    $('#digest_submit').click();
    equal($('#saved').text(), 'Saved!', "When #id_digest_active is not"+
                                        " checked, delete user's digest"+
                                        " settings and return success");

    $('#id_digest_active').prop('checked', 'checked');
    $('#digest_submit').click();
    equal($('#saved').text(), 'Something went wrong', "When #id_digest_active"+
                                                      " is checked and no"+
                                                      " email is provided,"+
                                                      " return an error"+
                                                      " condition");

    $('#id_digest_email').val('foo@example.com');
    $('#digest_submit').click();
    equal($('#saved').text(), 'Saved!', "When #id_digest_active is checked and"+
                                        " an email is provided, return"+
                                        " success");
});
