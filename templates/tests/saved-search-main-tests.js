module("saved-search-main.js Tests");
test("resize_modal", function() {
    $('#qunit-fixture').append($('<span />', { id:'foo' }));
    sizes = resize_modal('#foo');
    equal(sizes.length, 4, "resize_modal returns a list of four values");
    ok(sizes[0] > 0, "max_height must be positive");
    ok(sizes[1] < 0, "margin-top must be negative");
    ok(sizes[2] > 0, "width must be positive");
    ok(sizes[3] < 0, "margin-left must be negative");
});

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
                               { id: 'edit_modal' }));
    $.ajax = function(params) {
        if (params.url == 'edit' && params.data.csrfmiddlewaretoken == 'foo') {
            params.success('query successful');
        }
    };
    disable_fields = function(param1, param2) {
    };
    get_edit(1);
    $('#edit_modal').modal('hide');
    equal($('#edit_modal').html(), 'query successful', "AJAX response should"+
                                                       "be appended to #edit"+
                                                       "_modal");
});
test("save_form", function() {
    $('#qunit-fixture').append($('<div />',
                               { id: 'save_test' }));
    $('#save_test').append($('<form />',
                               { id: 'save_test_form' }));
    $('#save_test_form').append($('<input />',
                               { id: 'id_url', type: 'text' }));
    $('#save_test_form').append($('<span />',
                               { id: 'id_refresh' }));
    $('#save_test_form').append($('<input />',
                               { id: 'id_is_active', type: 'checkbox' }));
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
    equal($('#save_test_form').children().length, 3, "Form should have only"+
                                                     "three children");
    save_form('id_', 'save_test', 'foo_action', success_callback);
    equal($('#save_test_form').children().length, 4, "Form should have an"+
                                                     "error label added");
    $('#id_url').val('jobs.jobs/jobs');
    save_form('id_', 'save_test', 'foo_action', success_callback);
    equal($('#id_url').val(), '', "#id_url should be cleared");
    equal($('#id_is_active').checked, undefined, "#id_is_active should be"+
                                                 "cleared");
    equal($('#save_test_form').children().length, 3, "Error label should be"+
                                                     "removed");
});
test("validate", function() {
    $('#qunit-fixture').append($('<input />',
                               { id: 'id_url', type: 'text' }));
    $('#qunit-fixture').append($('<input />',
                               { id: 'id_feed', type: 'text' }));
    $('#qunit-fixture').append($('<input />',
                               { id: 'id_label', type: 'text' }));
    $('#qunit-fixture').append($('<div />', { id: 'id_validated' }));
    $.ajax = function(params) {
        if (params.data.url == 'jobs.jobs/jobs') {
            params.success('{"url_status":"valid","feed_title":"foo","rss_url"'+
                           ':"bar"}');
        } else {
            params.success('{"url_status":"fail"}');
        }
    }
    validate('id_', '');
    equal($('#id_validated').text(), 'fail', "Running validate with no feed"+
                                             "url returns 'fail'");
    equal($('#id_feed').text(), '', "With no url, #id_feed should be empty");
    equal($('#id_label').text(), '', "With no url, #id_label should be empty");

    $('#id_url').val('google.com');
    validate('id_', '');
    equal($('#id_validated').text(), 'fail', "Running validate with an invalid"+
                                             "feed url returns 'fail'");
    equal($('#id_feed').text(), '', "With an invalid url, #id_feed should be"+
                                    "empty");
    equal($('#id_label').text(), '', "With an invalid url, #id_label should be"+
                                     "empty");

    $('#id_url').val('jobs.jobs/jobs');
    validate('id_', '');
    equal($('#id_validated').text(), 'valid', "Running validate with a valid"+
                                              "url returns 'valid'");
    equal($('#id_feed').val(), 'bar', "With a valid url, #id_feed should get"+
                                      "set");
    equal($('#id_label').val(), 'foo', "With a valid url, #id_label should"+
                                       "get set");
});
test("save_digest_form", function() {
    $('#qunit-fixture').append($('<input />', { id: 'id_digest_active',
                                                type: 'checkbox' }));
    $('#qunit-fixture').append($('<input />', { id: 'id_digest_email',
                                                type: 'text' }));
    $('#qunit-fixture').append($('<input />', { id: 'id_send_if_none',
                                                type: 'checkbox' }));
    $('#qunit-fixture').append($('<span />', { id: 'saved' }));
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
    save_digest_form();
    equal($('#saved').text(), 'Saved!', "When #id_digest_active is not"+
                                        "checked, delete user's digest"+
                                        "settings and return success");

    $('#id_digest_active').prop('checked', 'checked');
    save_digest_form();
    equal($('#saved').text(), 'Something went wrong', "When #id_digest_active"+
                                                      "is checked and no email"+
                                                      "is provided, return"+
                                                      "error condition");

    $('#id_digest_email').val('foo@example.com');
    save_digest_form();
    equal($('#saved').text(), 'Saved!', "When #id_digest_active is checked and"+
                                        "an email is provided, return success");
});
