$(document).ready(function() {
    add_form();
    edit_form();
    cancel();
});

function add_form() {
    $('[id$="add"]').click(function(e) {
        e.preventDefault();
        var btn = $(this);
        var module = btn.attr('id').split("-")[0];
        $.ajax({
            url: '/profile/form/',
            data: {'module':module},
            success: function(data) {
                btn.hide();
                btn.after(data);
                cancel();
            }
        });
            
    });
};

function edit_form() {
    $('[id$="edit"]').click(function(e) {
        e.preventDefault();
        var item = $(this).parent();
        var module = $(this).attr('id').split("-")[0];
        var id = $(this).attr('id').split("-")[1];
        $.ajax({
            url: '/profile/form/',
            data: {'module':module, 'id':id},
            success: function(data) {
                item.hide();
                item.after(data);
                cancel();
            }
        });
            
    });
};

function cancel() {
    $('[id$="cancel"]').click(function(e) {
        e.preventDefault();
        var module =  $(this).attr('id').split('-')[0];
        var item_id = $(this).attr('id').split('-')[1];
        if (item_id != 'new') {
            $('#'+module+'-'+item_id+'-item').show();
        } else {
            $('#'+module+'-'+item_id+'-add').show();
        };
        $('#'+module+'-'+item_id+'-form').hide();
    });    
};
