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
    equal($('#saved').text(), 'Saved!',
          "When #id_digest_active is not checked, return success");

    $('#id_digest_active').prop('checked', 'checked');
    $('#digest_submit').click();
    equal($('#saved').text(), 'Something went wrong',
          "When #id_digest_active is checked and no email is provided, "+
          "return an error condition");

    $('#id_digest_email').val('foo@example.com');
    $('#digest_submit').click();
    equal($('#saved').text(), 'Saved!',
          "When #id_digest_active is checked and an email is provided, "+
          "return success");
});

module("saved-search-edit.js AJAX Tests", { setup: function() {
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
test("save_form", function() {
    $('#qunit-fixture').append($('<div />',
                               { id: 'save_test',
                                 'class': 'row' }));
    $('#save_test').append($('<form />',
                               { id: 'saved-search-form' }));
    var form = $('#saved-search-form')
    form.append($('<div />', { id: 'label-container' }));
    $('#label-container').append($('<label />',
                                     { 'for': 'id_url' }));
    form.append($('<input />',
                    { id: 'id_url',
                      type: 'text',
                      name: 'url' }));
    form.append($('<span />',
                    { id: 'id_refresh' }));
    form.append($('<input />',
                    { id: 'id_is_active',
                      type: 'checkbox',
                      name: 'is_active' }));
    form.append($('<a />',
                    { id: 'new_search',
                      'class': 'save',
                      'href': 'new' }));
    $('#id_is_active').prop('checked', true);
    $.ajax = function(params) {
        if (params.data.indexOf('wwww.my.jobs%2Fjobs') >= 0 &&
            params.data.indexOf('is_active=True') >= 0 &&
            params.data.indexOf('id=new') >= 0) {
            params.success('<td></td>');
        } else {
            params.success('{"url":["This field is required."]}');
        }
    };

    equal($('#id_url').parent().attr('id'), 'saved-search-form',
          "Before clicking, #id_url's parent should be the saved search form");
    $('#new_search').click();
    equal($('#id_url').parent().attr('class'), 'required',
          "After clicking, #id_url's parent should be a required field indicator");

    $('#id_url').val('www.my.jobs/jobs');
    $('#new_search').click();
    equal($('[class="label label-important"]').length, 0,
          "Error label should be removed");
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
        if (params.data.url == 'www.my.jobs/jobs') {
            params.success(
                '{"url_status":"valid","feed_title":"foo","rss_url":"bar"}');
        } else {
            params.success('{"url_status":"not valid"}');
        }
    }
    $('.refresh').click();
    equal($('#validated').text(), 'not valid',
          "Running validate with no feed url returns 'not valid'");
    equal($('#id_feed').text(), '', "With no url, #id_feed should be empty");
    equal($('#id_label').text(), '', "With no url, #id_label should be empty");

    $('#id_url').val('google.com');
    $('.refresh').click();
    equal($('#validated').text(), 'not valid',
          "Running validate with an invalid feed url returns 'not valid'");
    equal($('#id_feed').text(), '',
          "With an invalid url, #id_feed should be empty");
    equal($('#id_label').text(), '',
          "With an invalid url, #id_label should be empty");

    $('#id_url').val('www.my.jobs/jobs');
    $('.refresh').click();
    equal($('#validated').text(), 'valid',
          "Running validate with a valid url returns 'valid'");
    equal($('#id_feed').val(), 'bar',
          "With a valid url, #id_feed should get set");
    equal($('#id_label').val(), 'foo',
          "With a valid url, #id_label should get set");
});
