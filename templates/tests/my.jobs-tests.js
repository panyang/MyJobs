module("my.jobs.js Tests");
test("resize_modal", function() {
    $('#qunit-fixture').append($('<span />', { id:'foo' }));
    sizes = resize_modal('#foo');
    equal(sizes.length, 4, "resize_modal returns a list of four values");
    ok(sizes[0] > 0, "max_height must be positive");
    ok(sizes[1] < 0, "margin-top must be negative");
    ok(sizes[2] > 0, "width must be positive");
    ok(sizes[3] < 0, "margin-left must be negative");
});

