$(function() {
    var AppView = Backbone.View.extend({
        el: $(".row"),

        events: {
            "click [id$='section']": "addSection",
            // targets buttons within #moduleBank

            "click [id$='add']": "editForm",
            // targets "Add Another" buttons in each module section

            "click [id$='edit']": "editForm",
            // targets "Edit" buttons for individual modules

            "click [id$='cancel']": "cancelForm",
            // targets "Cancel" button in the modal window

            "hidden #edit_modal": "cancelForm",
            // targets event fired when #edit_modal is closed by means other
            // than the cancel button

            "click [id$='save']": "saveForm",
            // targets "Save" button  in the modal window

            "click [id$='delete']": "deleteItem",
            // targets "Delete" buttons for individual modules
        },

        /*
        Opens an empty module section (Name, Secondary Email, etc),
        allowing the user to add new modules to it

        :e: button contained within #moduleBank
        */
        addSection: function(e) {
            e.preventDefault();

            // id is formatted [module_type]-[item_id]
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

        /*
        Returns document to the state it was in prior to opening the form modal
        Called on "Cancel" button click or closure of the modal window

        :e: "Cancel" button within a modal or the modal itself
        */
        cancelForm: function(e) {
            e.preventDefault();

            var target;
            if (e.target.tagName.toLowerCase() == 'a') {
                // e is the modal cancel button; target it
                target = $(e.target)
            } else {
                // e is the modal itself; target its cancel button instead
                target = $(e.target).find('a[id$="cancel"]');
            }
            // id is formatted [module_type]-[item_id]-[event]
            var module = target.attr('id').split('-')[0];
            var item_id = target.attr('id').split('-')[1];

            // Upon closing the modal window, it should be removed from the
            // document to allow for additional modals
            $("div#edit_modal").remove();
            if (item_id != 'new') {
                // When "Edit" was clicked, the relevant item was hidden
                // Since nothing has changed, the item needs to be re-shown
                $('#'+module+'-'+item_id+'-item').show();
            }
        },

        /*
        Retrieves the desired form via AJAX, adds the modal form to the
        document, and displays the form

        :e: "Add Another" button for the current module section
             or "Edit" button associated with the item to be edited
        */
        editForm: function(e) {
            e.preventDefault();

            // id is formatted [module_type]-[item_id]-[event]
            var module = $(e.target).attr('id').split("-")[0];
            var id = $(e.target).attr('id').split("-")[1];
            var item;
            if (id != 'new') {
                // targets the table row containing the item to be edited
                item = $(e.target).parents('tr');
            }

            // targets the "Add Another" button for the current module section
            var button = $(e.target).parents('.formBox').children('button[id$="add"]')
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

        /*
        Saves both new and edited modules

        :e: "Save" button within a modal
        */
        saveForm: function(e) {
            e.preventDefault();

            // id is formatted [module_type]-[item_id]-[event]
            var module =  $(e.target).attr('id').split('-')[0];
            var item_id = $(e.target).attr('id').split('-')[1];

            // targets the form contained in the modal window
            var form = $('#edit_modal form');

            // targets the item table in the current module section
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
            var serialized_data = form.serialize();
            serialized_data += '&module=' + module + '&id=' + item_id +
                               '&first_instance=' + first_instance +
                               '&csrfmiddlewaretoken=' + csrf_token;
            $.ajax({
                type: 'POST',
                url: '/profile/form/',
                data: serialized_data,
                success: function(data) {
                    if (data.indexOf('<td>') >= 0) {
                        // form was valid; data should be appended to the table
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
                        // form was a json-encoded list of errors
                        var json = jQuery.parseJSON(data);

                        // remove current errors
                        $('[class*=label-important]').remove();
                        for (var i=0; i<json.length; i++) {
                            // insert new errors after the relevant inputs
                            $('[id$="-'+json[i]+'"]').after('<span class="label label-important">Required</span>');
                        }
                    }
                }
            });            
        },

        /*
        Deletes the specified item

        :e: "Delete" button associated with the item to be deleted
        */
        deleteItem: function(e) {
            e.preventDefault();
            csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
            var csrf_token = "";
            if(typeof(csrf_token_tag)!='undefined'){
                csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            }

            // targets the table row containing the item to be deleted
            var item = $(e.target).parents('tr');

            // id is formatted [module_type]-[item_id]-[event]
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
                        // The last item in a module section was deleted

                        // id is formatted [module_type]-items
                        parent_name = parent.parents(".formBox").attr("id").split("_")[0];

                        // Remove the empty section
                        parent.parents(".formBox").remove();

                        // Replace the button within the #moduleBank table
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
