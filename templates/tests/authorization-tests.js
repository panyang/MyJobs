var ajax;
module("authorization.js Tests - Login", {
    setup: function() {
        var fixture = $('#qunit-fixture');
        var form = $('<form />', {id: 'auth-form',
                                  action: ''});
        form.append($('<input />', { name: 'csrfmiddlewaretoken',
                                     value: 'foo' }));
        form.append($('<input />', {type: 'text',
                                    id: 'id_username',
                                    name: 'username',
                                    value: 'wrong@example.com'}));
        form.append($('<input />', {type: 'password',
                                    id: 'id_password',
                                    name: 'password',
                                    value: 'wrongpass'}));
        form.append($('<button />', {id: 'auth-login',
                                     type: 'submit'}));
        fixture.append(form)

        ajax = $.ajax;
        $.ajax = function(params) {
            var scratch = params.data.split('&');
            var data = {};
            for (var index = 0; index < scratch.length; index++) {
                scratch[index] = scratch[index].split('=');
                data[scratch[index][0]] = scratch[index][1]
            }
            if (data.username == 'alice%40example.com') {
                if (data.password == 'secret') {
                    params.success('{"url":"http://jobs.jobs/?key=key_here"}', 'prevent-redirect');
                } else {
                    params.success('{"errors":[["password",["Required"]]]}');
                }
            } else {
                if (data.password == 'secret') {
                    params.success('{"errors":[["username",["Required"]]');
                } else {
                    params.success('{"errors":[["password",["Required"]],["username",["Required"]]]}');
                }
            }
        }
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test('invalid form', function() {
    expect(4)

    equal($('.required-border').length, 0,
          'before clicking, no inputs have error markup');

    // When save is clicked and parameters are incorrect,
    // errors should be added to the form
    $('button#auth-login').click();
    equal($('.required-border').length, 2,
          'two errors should have been added');

    $('#id_username').val('alice@example.com');

    $('button#auth-login').click();
    equal($('.required-border').length, 1,
          'one error should have been removed');

    $('#id_password').val('secret');

    $('button#auth-login').click();
    equal($('.required-border').length, 0,
          'all errors should have been removed');
});
