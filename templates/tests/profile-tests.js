var ajax;
module("profile.js Tests - saveForm", {
    setup: function() {
        var fixture = $('#qunit-fixture');
        fixture.append($('<form/>', {id: 'profile-unit-form'}));
        $('#qunit-fixture').append($('<input />',
                                   { name: 'csrfmiddlewaretoken',
                                     value: 'foo' }));
        var form = $('form');
        form.append($('<input />', {type: 'hidden',
                                     name: 'csrfmiddlewaretoken',
                                     value: 'foo'}));
        form.append($('<input />', {type: 'text',
                                    id: 'id_name-given_name',
                                    name: 'given_name',
                                    value: ''}));
        form.append($('<input />', {type: 'text',
                                    id: 'id_name-family_name',
                                    name: 'family_name',
                                    value: ''}));
        form.append($('<button />', {id: 'Name-new-save',
                                     type: 'submit'}));

        ajax = $.ajax;
        $.ajax = function(params) {
            if (params.url == '/profile/edit/' &&
                params.data == 'csrfmiddlewaretoken=foo&given_name=Alice&family_name=Smith') {
                params.success('', 'prevent-redirect');
            } else {
                params.success('{"given_name":["This field is required"],"family_name":["This field is required"]}');
            }
        }
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("name values are missing", function() {
    expect(2);

    equal($('[class*="required"]').length, 0,
          'before clicking, no inputs have error markup');

    // When save is clicked and parameters are incorrect,
    // errors should be added to the form
    $('button[id$="save"]').click();
    equal($('[class*="required"]').length, 2,
          'two errors should have been added');
});

module("profile.js Tests - getSelect", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<label />', {'for': 'foo-country_code'}));
        fixture.append($('<input />', {type: 'hidden',
                                       value: 'USA',
                                       id: 'foo-country_code'}));
        fixture.append($('<label />',
                       {'for': 'foo-country_sub_division_code'}));
        fixture.append($('<input />',
                       {type: 'hidden',
                        id: 'foo-country_sub_division_code'}));

        ajax = $.ajax;

        $.ajax = function(params) {
            if (params.url.indexOf('usa_regions.jsonp') > -1) {
                params.success({"regions": [{"code": "AZ", "name": "Arizona"}],
                                "friendly_label": "State",
                                "default_option": "az"});
            }
        }
    }, teardown: function() {
        $.ajax = ajax;
    }
});
