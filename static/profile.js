$(function() {
    var AppView = Backbone.View.extend({
        el: $(".row"),

        events: {
            "click [id$='section']": "addSection",
            "click [id$='add']": "editForm",
            "click [id$='cancel']": "cancelForm",
            "hidden #edit_modal": "cancelForm",
            "click [id$='edit']": "editForm",
            "click [id$='save']": "saveForm",
            "click [id$='delete']": "deleteItem",
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

        cancelForm: function(e) {
            e.preventDefault();
            var target;
            if (e.target.tagName.toLowerCase() == 'a') {
                target = $(e.target)
            } else {
                target = $(e.target).parents('.formBox').find('tr:hidden')
            }
            var module = target.attr('id').split('-')[0];
            var item_id = target.attr('id').split('-')[1];
            $("div#edit_modal").remove();
            var action;
            if (item_id != 'new') {
                $('#'+module+'-'+item_id+'-item').show();
            }
        },

        editForm: function(e) {
            e.preventDefault();

            var module = $(e.target).attr('id').split("-")[0];
            var id = $(e.target).attr('id').split("-")[1];
            var item;
            if (id != 'new') {
                item = $(e.target).parent().parent();
            }
            var button = $(e.target).parents('.formBox').children('button')
            $.ajax({
                url: '/profile/form/',
                data: {'module':module, 'id':id},
                success: function(data) {
                    if (item) {
                        item.hide();
                    }
                    button.before(data);
                    $('#edit_modal').modal();
                    datepicker();
                }
            });            
        },

        saveForm: function(e) {
            e.preventDefault();
            var module =  $(e.target).attr('id').split('-')[0];
            var item_id = $(e.target).attr('id').split('-')[1];
            var form = $('#edit_modal form');
            var table = $(e.target).parents('.formBox').children('table')

            csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
            var csrf_token = "";
            if(typeof(csrf_token_tag)!='undefined'){
                csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            }

            first_instance=0;
            if(typeof(table.attr("class"))=="undefined"){
                first_instance = 1;
            }  
            console.log(first_instance)    
            var serialized_data = form.serialize() + '&module=' + module + '&id=' + item_id + '&first_instance=' + first_instance + '&csrfmiddlewaretoken=' + csrf_token;
            $.ajax({
                type: 'POST',
                url: '/profile/form/',
                data: serialized_data,
                success: function(data) {
                    if (data.indexOf('<td>') >= 0) {
                        if (first_instance) {
                            $(e.target).parents('.formBox').children('h4').after(
                                '<table class="table table-bordered table-striped"></table>'
                                );
                            table = $(e.target).parents('.formBox').children('table')
                        }
                        table.append(data);
                        $('#'+module+'-'+item_id+'-item').remove();
                        $('#edit_modal').modal('hide');
                    } else {
                        var json = jQuery.parseJSON(data);
                        $('[class*=label-important]').remove();
                        for (var i=0; i<json.length; i++) {
                            $('[id$="-'+json[i]+'"]').after('<span class="label label-important">Required</span>');
                        }
                    }
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

        closeEdit: function(e) {
            e.preventDefault();
        },
    });

    var App = new AppView;
});

function datepicker() {
    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd"});
    });
};
