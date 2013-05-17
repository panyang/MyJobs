var ajax, disable;
module("profile.js Tests", { setup: function() {
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
test("addSection", function() {
    var fixture = $('#qunit-fixture');
    fixture.append($('<div />', { id: 'moduleBank' }));
    fixture.append($('<button />', { id: 'Name-new-section'}));
    fixture.append($('<div />', { id: 'moduleColumn'}));
    expect(3)

    $.ajax = function(params) {
        if (params.url == '/profile/section/' && params.data.module == 'Name') {
            params.success('<div id="Name_items"><button id="Name-new-add"></button></div>')
        } else if (params.url == '/profile/form/' && params.data.module == 'Name' && params.data.id == 'new') {
            ok(1, 'Add button clicked');
        }
    };

    equal($('#moduleBank:visible').length, 1, "moduleBank is visible")
    $('[id$="section"]').click();
    equal($('#moduleBank:visible').length, 0, "moduleBank was hidden")
});

test("editForm", function() {
});
