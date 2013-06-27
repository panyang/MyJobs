var ajax;
module("profile.js Tests - addSection", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', { id: 'moduleBank' }));
        fixture.append($('<div />', { id: 'moduleColumn'}));
        $('#moduleBank').append($('<table />'));
        $('#moduleBank table').append($('<tbody />'));
        $('#moduleBank table tbody').append($('<tr />', {'class': 'profile-section'}));
        $('.profile-section').append($('<button />', { id: 'Name-new-section'}));

        ajax = $.ajax;

        $.ajax = function(params) {
            if (params.url == '/profile/form/' &&
                params.data.module == 'Name') {
                // params are correct; return a new profile section
                params.success('<div id="Name_items"><h4></h4><button '+
                               'id="Name-new-add"></button></div>')
            }
        };
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("adding a new module section", function() {
    expect(6);

    // Before click: #moduleBank is visible and has one child
    //               #Name_items does not exist
    equal($('#moduleBank:visible').length, 1, 'moduleBank is visible');
    equal($('#moduleBank').children().length, 1, 'moduleBank has one child');
    equal($('#Name_items').length, 0, 'Name_items does not exist yet');

    $('[id$="section"]').click();
    // After click: #moduleBank is not visible and has no children
    //              #Name_items exists
    equal($('#moduleBank').length, 1, 'moduleBank still exists');
    equal($('#moduleBank:visible').length, 0, 'moduleBank is hidden');
    equal($('#moduleColumn').children().attr('id'), 'Name_items',
          'Name_items should be appended to moduleColumn');
});

module("profile.js Tests - editForm", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', { id: 'moduleColumn'}));
        $('#moduleColumn').append($('<div />', {id: 'Name_items'}));
        $('#Name_items').append('<table><tbody><tr id="table_tr"></tr></tbody></table>');
        $('#table_tr').append($('<button />', {id: 'Name-new-add'}));

        ajax = $.ajax;

        $.ajax = function(params) {
            if (params.url == '/profile/form/' && params.data.module == 'Name' &&
                params.data.id == 'new') {
                // params are correct; return a new "modal"
                params.success('<div id="edit_modal"></div>');
            }
        }
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("adding a new profile item", function() {
    expect(3);

    //Before click: #edit_modal does not exist
    equal($('#edit_modal').length, 0, 'edit_modal should not exist yet');

    $('[id$="add"]').click();
    //After click: #edit_modal exists and is visible
    equal($('#edit_modal').length, 1,
        'edit_modal should be appended to moduleColumn');
    equal($('#edit_modal:visible').length, 1, 'edit_modal is visible');
    $('#edit_modal').modal('hide');
});

module("profile.js Tests - cancelForm", {
    setup: function() {
        var fixture = $('#qunit-fixture')
        fixture.append($('<div />', {id: 'foo_modal'}));
        $('#foo_modal').append($('<a />', {id: 'Name-1-cancel',
                                           'data-dismiss': 'modal',
                                           'class': 'modal hide fade'}));
        fixture.append($('<div />', {id: 'background_modal'}));
    }
});
test("canceling an active modal", function() {
    expect(5);

    // When cancel is clicked but modals exist and are visible,
    // nothing should happen
    $('[id$="modal"]').modal();
    equal($('[id$="modal"]:visible').length, 2, 'both modals are visible');
    $('[id$="cancel"]').click();
    equal($('[id$="modal"]').length, 2, 'there are two modals');
    equal($('[id$="modal"]:visible').length, 1, 'one modal is visible');
    $('#foo_modal').modal();
    $('#background_modal').modal('hide');

    // When cancel is clicked and no modals are visible,
    // modals should be removed
    equal($('[id$="modal"]:visible').length, 1, 'one modal should still be visible');
    $('[id$="cancel"]').click();
    equal($('[id$="modal"]').length, 0, 'all modals have been removed');
});

module("profile.js Tests - saveForm", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', { id: 'moduleColumn'}));
        fixture.append($('<div />', {id: 'edit_modal'}));
        $('#moduleColumn').append($('<div />', {id: 'Name_items'}));
        $('#Name_items').append($('<h4 />'));
        $('#qunit-fixture').append($('<input />',
                                   { name: 'csrfmiddlewaretoken',
                                     value: 'foo' }));
        var modal = $('#edit_modal');
        modal.append($('<input />', {type: 'hidden',
                                     name: 'csrfmiddlewaretoken',
                                     value: 'foo'}));
        modal.append($('<form />', {id: 'save_form'}));
        var form = $('#save_form');
        form.append($('<input />', {type: 'hidden',
                                    id: 'id-given_name',
                                    name: 'given_name',
                                    value: 'Alice'}));
        form.append($('<input />', {type: 'hidden',
                                    id: 'id-family_name',
                                    name: 'family_name',
                                    value: 'Smith'}));
        modal.append($('<a />', {id: 'Name-new-save'}));
        $('#edit_modal').modal()

        ajax = $.ajax;

        $.ajax = function(params) {
            if (params.url == '/profile/form/' &&
                params.data == 'given_name=Alice&family_name=Smith&module='+
                               'Name&id=new&first_instance=1'+
                               '&csrfmiddlewaretoken=foo') {
                params.success('<tr id="Name-1-item"><td>foo</td></tr>')
            } else {
                params.success('{"errors":[["given_name",["This field is required"]],["family_name",["This field is required"]]]}');
            }
        }
    }, teardown: function() {
        $('#edit_modal').modal('hide');

        $.ajax = ajax;
    }
});
test("all data is provided and valid", function() {
    expect(5);

    equal($('#Name_items').children().length, 1,
          'Name_items should have only one child');
    equal($('#Name_items').html(), '<h4></h4>',
          "Name_items's child should be a single h4 element");
    equal($('#Name_items table tr').length, 0,
          'there should be no table rows');

    // When save is clicked and parameters are correct,
    // a new row should be added
    $('a[id$="save"]').click();
    equal($('#Name_items table tr').length, 1,
          'after clicking, there should be one row');
    equal($('#Name_items').children().length, 2,
          'after clicking, Name_items should have two children');
});
test("name values are missing", function() {
    $('[name$="name"]').val('');

    expect(5);

    equal($('#Name_items').children().length, 1,
          'Name_items should have only one child');
    equal($('#Name_items').html(), '<h4></h4>',
          "Name_items's child should be an h4 element");
    equal($('#Name_items table tr').length, 0,
          'there should be no table rows');

    // When save is clicked and parameters are incorrect,
    // errors should be added to the modal
    $('a[id$="save"]').click();
    equal($('#Name_items table tr').length, 0,
          'after clicking, there should still be no rows');
    equal($('[class*="required"]').length, 2,
          'errors should have been added');
});

module("profile.js Tests - deleteItem", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', { id: 'moduleBank' }));
        fixture.append($('<div />', { id: 'moduleColumn'}));
        $('#moduleBank').append($('<table />'));
        $('#moduleBank table').append($('<tbody />'));
        $('#moduleBank table tbody').append($('<tr />', {id: 'table_tr'}));
        $('#moduleColumn').append($('<div />', {id: 'Name_items'}));
        $('#Name_items').append($('<h4 />'));
        $('#qunit-fixture').append($('<input />',
                                   { name: 'csrfmiddlewaretoken',
                                     value: 'foo' }));

        ajax = $.ajax;

        $.ajax = function(params) {
            if (params.url == '/profile/delete/' &&
                params.data.module == 'Name' &&
                params.data.id == '1' &&
                params.data.csrfmiddlewaretoken == 'foo') {
                ok(1, 'params are okay');
                params.success();
            } else {
                ok(0, 'params are not okay');
            }
        }
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("deleting an item", function() {
    var fixture = $('#qunit-fixture');
    fixture.append($('<div />', {id: 'modal'}));
    var modal = $('#modal');
    modal.append($('<input />', {name: 'csrfmiddlewaretoken',
                                 value: 'foo'}));
    modal.append($('<a />', {id: 'Name-1-delete'}));
    $('#Name_items').append('<table><tbody><tr id="Name-1-item">'+
                            '</tr></tbody></table>');

    expect(3);

    equal($('#Name_items table tbody tr').length, 1,
          'there should be one tr element');
    $('#Name-1-delete').click();
    equal($('#Name_items table tbody tr').length, 0,
          'there should be no tr elements remaining');
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

module("profile.js Tests - confirmDelete", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', {id: 'confirm_modal'}));
        fixture.append($('<a />', {id: 'delete_confirm'}));
    }
});
test("confirming module deletion", function() {
    expect(2);

    $('#confirm_modal').hide();
    equal($('#confirm_modal:visible').length, 0,
          'confirm_modal should not be visible');
    $('#delete_confirm').click();
    equal($('#confirm_modal:visible').length, 1,
          'confirm_modal should be visible');
    $('#confirm_modal').modal('hide');
});

module("profile.js Tests - viewDetails", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', { id: 'moduleColumn'}));
        $('#moduleColumn').append($('<div />', {id: 'Name_items'}));
        $('#Name_items').append($('<h4 />'));
        $('#Name_items').append($('<table />', {id: 'view_table'}));
        $('#view_table').append($('<tr />'));
        $('#view_table tr').append($('<a />', {id: 'Name-1-view'}));

        ajax = $.ajax;

        $.ajax = function(params) {
            if (params.url == '/profile/details/' &&
                params.data.module == 'Name' &&
                params.data.id == '1') {
                params.success('<div id="detail_modal"></div>');
            }
        }
    }, teardown: function() {
        $.ajax = ajax;
        $('#detail_modal').modal('hide');
    }
});
test("viewing module details", function() {
    expect(4);

    equal($('#view_table').next().length, 0,
          'table should not be followed by other elements');
    $('#Name-1-view').click();
    equal($('#view_table').next().length, 1,
          'table should be followed by one element');
    equal($('#view_table').next().attr('id'), 'detail_modal',
          'the element following table should be #detail_modal');
    equal($('#detail_modal:visible').length, 1,
          'detail_modal should be visible');
});
