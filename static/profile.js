$(function() {
    var AppView = Backbone.View.extend({
        el: $(".formBox"),

        events: {
            "click [id$='add']": "showForm",
            "click [id$='cancel']": "cancelForm",
            "click [id$='edit']": "editForm",
            "click [id$='save']": "saveForm",
            "click [id$='delete']": "deleteItem"
        },
        
        showForm: function(e) {

            var btn = $(e.target);
            var module = btn.attr('id').split("-")[0];
            $.ajax({
                url: '/profile/form/',
                data: {'module':module},
                success: function(data) {
                    btn.hide();
                    btn.after(data);
                    datepicker();
                }
            });
        },

        cancelForm: function(e) {
            e.preventDefault();
            var module =  $(e.target).attr('id').split('-')[0];
            var item_id = $(e.target).attr('id').split('-')[1];
            if (item_id != 'new') {
                $('#'+module+'-'+item_id+'-item').show();
            } else {
                $('#'+module+'-'+item_id+'-add').show();
            };
            $('#'+module+'-'+item_id+'-form').hide();
        },

        editForm: function(e) {
            e.preventDefault();

            var item = $(e.target).parent();
            var module = $(e.target).attr('id').split("-")[0];
            var id = $(e.target).attr('id').split("-")[1];
            $.ajax({
                url: '/profile/form/',
                data: {'module':module, 'id':id},
                success: function(data) {
                    item.hide();
                    item.after(data);
                    datepicker();
                }
            });            
        },

        saveForm: function(e) {
            e.preventDefault();
            var module =  $(e.target).attr('id').split('-')[0];
            var item_id = $(e.target).attr('id').split('-')[1];
            var form = $(e.target).parents('form');
            var serialized_data = form.serialize() + '&module=' + module + '&id=' + item_id;
            $.ajax({
                type: 'POST',
                url: '/profile/form/',
                data: serialized_data,
                success: function(data) {
                    $(e.target).append(data);
                }
            });            
        },

        deleteItem: function(e) {
            e.preventDefault();
            csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
            var csrf_token = "";
            if(typeof(csrf_token_tag)!='undefined'){
                csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            }

            var item = $(e.target).parent();
            var module = $(e.target).attr('id').split("-")[0];
            var id = $(e.target).attr('id').split("-")[1];
            $.ajax({
                type: 'POST',
                url: '/profile/delete/',
                data: {'module':module, 'id':id, csrfmiddlewaretoken: csrf_token},
                success: function(data) {
                    item.remove();
                }
            });            
            
        }     
    });

    var App = new AppView;
});

function datepicker() {
    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd"});
    });
};
