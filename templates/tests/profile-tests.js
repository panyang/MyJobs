var ajax;
module("profile.js Tests - addSection", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', { id: 'moduleBank' }));
        fixture.append($('<div />', { id: 'moduleColumn'}));
        $('#moduleBank').append($('<table />'));
        $('#moduleBank table').append($('<tbody />'));
        $('#moduleBank table tbody').append($('<tr />', {id: 'table_tr'}));
        $('#table_tr').append($('<button />', { id: 'Name-new-section'}));
        $('#qunit-fixture').append($('<input />',
                                   { name: 'csrfmiddlewaretoken',
                                     value: 'foo' }));

        ajax = $.ajax;

        $.ajax = function(params) {
            if (params.url == '/profile/section/' &&
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
test("good data", function() {
    expect(3);

    equal($('#moduleBank:visible').length, 1, "moduleBank is visible");
    $('[id$="section"]').click();
    equal($('#moduleBank:visible').length, 0, "moduleBank is hidden");
    equal($('#moduleColumn').children().attr('id'), 'Name_items',
          'Name_items should be appended to moduleColumn');
});

module("profile.js Tests - editForm", {
    setup: function() {
        // insert document structure common to all tests
        var fixture = $('#qunit-fixture');
        fixture.append($('<div />', { id: 'moduleColumn'}));
        $('#moduleColumn').append($('<div />', {id: 'Name_items'}));
        $('#Name_items').append($('<h4 />'));
        $('#Name_items').append('<table><tbody><tr id="table_tr"></tr></tbody></table>');
        $('#table_tr').append($('<button />', {id: 'Name-new-add'}));
        $('#qunit-fixture').append($('<input />',
                                   { name: 'csrfmiddlewaretoken',
                                     value: 'foo' }));

        ajax = $.ajax;
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("good data", function() {
    expect(2);

    $.ajax = function(params) {
        if (params.url == '/profile/form/' && params.data.module == 'Name' &&
            params.data.id == 'new') {
            // params are correct; return a new "modal"
            params.success('<div id="edit_modal"></div>');
        }
    }

    $('[id$="add"]').click();
    equal($('#moduleColumn').children('#edit_modal').length, 1,
       'edit_modal should be appended to moduleColumn');
    equal($('#edit_modal:visible').length, 1, 'edit_modal is visible');
    $('#edit_modal').modal('hide');
});

module("profile.js Tests - cancelForm", {
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
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("good data", function() {
    var fixture = $('#qunit-fixture')
    fixture.append($('<div />', {id: 'foo_modal'}));
    $('#foo_modal').append($('<a />', {id: 'Name-1-cancel',
                                       'data-dismiss': 'modal'}));
    fixture.append($('<div />', {id: 'background_modal'}));

    expect(4);

    // When cancel is clicked but modals exist and are visible,
    // nothing should happen
    $('[id$="cancel"]').click();
    equal($('[id$="modal"]').length, 2, 'there are two modals');
    equal($('[id$="modal"]:visible').length, 2, 'both modals are visible');

    // When cancel is clicked and no modals are visible,
    // modals should be removed
    $('[id$="modal"]').hide();
    equal($('[id$="modal"]:visible').length, 0, 'all modals should be hidden');
    $('[id$="cancel"]').click();
    equal($('[id$="modal"]').length, 0, 'all modals have been removed');
});

module("profile.js Tests - saveForm", {
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
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("good data", function() {
    $('table').remove();
    var fixture = $('#qunit-fixture');
    fixture.append($('<div />', {id: 'edit_modal'}));
    var modal = $('#edit_modal');
    modal.append($('<input />', {type: 'hidden',
                                 name: 'csrfmiddlewaretoken',
                                 value: 'foo'}));
    modal.append($('<form />', {id: 'save_form'}));
    var form = $('#save_form');
    form.append($('<input />', {type: 'hidden',
                                name: 'name',
                                value: 'Alice'}));
    modal.append($('<a />', {id: 'Name-new-save'}));

    expect(5);

    $.ajax = function(params) {
        if (params.url == '/profile/form/' &&
            params.data == 'name=Alice&module=Name&id=new&first_instance=1'+
                           '&csrfmiddlewaretoken=foo') {
            ok(1, 'parameters are okay');
            params.success('<tr id="Name-1-item"><td>foo</td></tr>')
        } else {
            ok(0, 'parameters are not okay');
        }
    }

    $('#edit_modal').modal()
    equal($('#Name_items').children().length, 1,
          'Name_items should have only one child');
    equal($('#Name_items').html(), '<h4></h4>',
          "Name_items's child should be an h4 element");
    equal($('#Name_items table tr').length, 0,
          'there should be no table rows');

    // When save is clicked and parameters are correct,
    // a new row should be added
    $('a[id$="save"]').click();
    equal($('#Name_items table tr').length, 1,
          'after clicking, there should be one row');
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
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("good data", function() {
    var fixture = $('#qunit-fixture');
    fixture.append($('<div />', {id: 'modal'}));
    var modal = $('#modal');
    modal.append($('<input />', {name: 'csrfmiddlewaretoken',
                                 value: 'foo'}));
    modal.append($('<a />', {id: 'Name-1-delete'}));
    $('#Name_items').append('<table><tbody><tr id="Name-1-item">'+
                            '</tr></tbody></table>');

    expect(3);

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
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("good data", function() {
    $('#qunit-fixture').children().remove();
    $('#qunit-fixture').append($('<label />', {'for': 'foo-country_code'}));
    $('#qunit-fixture').append($('<input />', {type: 'hidden',
                                               value: 'USA',
                                               id: 'foo-country_code'}));
    $('#qunit-fixture').append($('<label />',
                               {'for': 'foo-country_sub_division_code'}));
    $('#qunit-fixture').append($('<input />',
                               {type: 'hidden',
                                id: 'foo-country_sub_division_code'}));
    expect(3);

    $.ajax = function(params) {
        if (params.url.indexOf('usa_regions.jsonp') > -1) {
            ok(1, 'retrieving usa_regions.jsonp');
            params.success({"regions": [{"code": "AZ", "name": "Arizona"}],
                            "friendly_label": "State",
                            "default_option": "az"});
        } else {
            ok(0, 'retrieving wrong jsonp file');
        }
    }

    // foo-country_sub_division_code should not have a value until
    // foo-country_code has triggered the change event
    equal($('[id$="-country_sub_division_code"]').val(), '',
          'nothing should be selected');
    $('[id$="-country_code"]').trigger('change')
    equal($('[id$="-country_sub_division_code"]').val(), 'AZ',
          'AZ should be selected');
});

module("profile.js Tests - confirmDelete", {
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
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("good data", function() {
    var framework = $('#qunit-fixture');
    framework.append($('<div />', {id: 'confirm_modal'}));
    framework.append($('<a />', {id: 'delete_confirm'}));
    
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
    }, teardown: function() {
        $.ajax = ajax;
    }
});
test("good data", function() {
    $('#qunit-fixture').append($('<table />', {id: 'view_table'}));
    $('#view_table').append($('<a />', {id: 'Name-1-view'}));

    expect(5);

    $.ajax = function(params) {
        if (params.url == '/profile/details/' &&
            params.data.module == 'Name' &&
            params.data.id == '1') {
            ok(1, 'params are okay');
            params.success('<div id="detail_modal"></div>');
        } else {
            ok(0, 'params are not okay');
        }
    }

    equal($('#view_table').next().length, 0,
          'table should not be followed by other elements');
    $('#Name-1-view').click();
    equal($('#view_table').next().length, 1,
          'table should be followed by one element');
    equal($('#view_table').next().attr('id'), 'detail_modal',
          'the element following table should be #detail_modal');
    equal($('#detail_modal:visible').length, 1,
          'detail_modal should be visible');
    $('#detail_modal').modal('hide');
});
