$(function() {
    var AppView = Backbone.View.extend({
        el: $(".row"),

        events: {
            "click [id$='section']": "addSection",
            "click [id$='add']": "showForm",
            "click [id$='cancel']": "cancelForm",
            "click [id$='edit']": "editForm",
            "click [id$='save']": "saveForm",
            "click [id$='delete']": "deleteItem"
        },

        
        addSection: function(e) {
            e.preventDefault();
            var module = $(e.target).attr('id').split('-')[0];
            $.ajax({
                url: '/profile/section/',
                data: {'module': module},
                success: function(data) {
                    $(e.target).remove();
                    $('#moduleColumn').append(data);
                }
            });
        },

        showForm: function(e) {
            var btn = $(e.target);
            var module = btn.attr('id').split("-")[0];
            var table = $(e.target).parents('.formBox').children('table')
            $.ajax({
                url: '/profile/form/',
                data: {'module':module},
                success: function(data) {
                    btn.hide();
                    btn.before(data);
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
            $('#'+module+'-'+item_id+'-form').remove();
        },

        editForm: function(e) {
            e.preventDefault();

            var item = $(e.target).parent().parent();
            var module = $(e.target).attr('id').split("-")[0];
            var id = $(e.target).attr('id').split("-")[1];
            var table = $(e.target).parents('.formBox').children('table')
            $.ajax({
                url: '/profile/form/',
                data: {'module':module, 'id':id},
                success: function(data) {
                    item.hide();
                    table.after(data);
                    datepicker();
                }
            });            
        },

        saveForm: function(e) {
            e.preventDefault();
            var module =  $(e.target).attr('id').split('-')[0];
            var item_id = $(e.target).attr('id').split('-')[1];
            var form = $(e.target).parents('form');
            var table = $(e.target).parents('.formBox').children('table')
            first_instance=0;
            if(typeof(table.attr("class"))=="undefined"){
                first_instance = 1;
                $(e.target).parents('.formBox').children('h4').after(
                    '<table class="table table-bordered table-striped"></table>'
                    );
                table = $(e.target).parents('.formBox').children('table')
            }  
            console.log(first_instance)    
            var serialized_data = form.serialize() + '&module=' + module + '&id=' + item_id + '&first_instance=' + first_instance;
            $.ajax({
                type: 'POST',
                url: '/profile/form/',
                data: serialized_data,
                success: function(data) {
                    if (item_id == 'new') {
                        form.siblings("[id$='add']").show();
                    };
                    form.replaceWith("");
                    table.append(data);                    
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

            var item = $(e.target).parent().parent();
            var module = $(e.target).attr('id').split("-")[0];
            var id = $(e.target).attr('id').split("-")[1];
            $.ajax({
                type: 'POST',
                url: '/profile/delete/',
                data: {'module':module, 'id':id, csrfmiddlewaretoken: csrf_token},
                success: function(data) {
                    parent = item.parents("table");
                    item.remove();
                    if (parent.find("tr").length <=1 ){
                        parent_name = parent.parents(".formBox").attr("id").split("_")[0] 
                        parent.parents(".formBox").remove();
                        $("#moduleBank table").append(
                            "<tr class='profile_section'><td><a id='"+parent_name+"-section' href=''>"+parent_name+"</a></td></tr>"
                        );
                    }
                }
            });
        },
    });

    var App = new AppView;
});

function datepicker() {
    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd"});
    });
};
