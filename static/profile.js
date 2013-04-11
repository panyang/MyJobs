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

            "hidden #edit_modal": "cancelForm",
            // targets event fired when #edit_modal is closed
            // includes clicking any of the modal close buttons, pressing Esc,
            // and clicking on the dark modal background

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
                    $(e.target).parents('tr').remove();
                    if ($('#moduleBank').find('tr').length == 0) {
                        $('#moduleBank').hide();
                    }
                    data = $(data).hide();
                    $('#moduleColumn').append(data);
                    module_elem = $('#'+module+'_items');
                    module_elem.find('[id$="add"]').click();
                }
            });
        },

        /*
        Returns document to the state it was in prior to opening the form modal
        Called on "Cancel" button click or closure of the modal window

        :e: new/edit module modal window
        */
        cancelForm: function(e) {
            e.preventDefault();

            // targets the cancel button located within the modal window
            var target = $(e.target).find('a[id$="cancel"]');

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
            } else {
                manageModuleDisplay(module);
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
            $.ajax({
                url: '/profile/form/',
                data: {'module':module, 'id':id},
                success: function(data) {
                    if (item) {
                        item.hide();
                    }
                    data = $(data).hide();
                    $('#moduleColumn').append(data);
                    resize_modal('#edit_modal');
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
            var table = $('#'+module+'_items').children('table')

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
                            $('#'+module+'_items').children('h4').after(
                                '<table class="table table-bordered table-striped"></table>'
                            );
                            table = $('#'+module+'_items').children('table')
                        }
                        table.append(data);
                        $('#'+module+'-'+item_id+'-item').remove();
                        $('#edit_modal').modal('hide');
                        $('#'+module+'_items').show();
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
                    item.remove();
                    manageModuleDisplay(module);
                }
            });
        },
    });

    var App = new AppView;

    $(window).on('resize', function() {
        resize_modal('#edit_modal');
    });
});

function manageModuleDisplay(module) {
    var target = $('#'+module+'_items');
    if (target.find('table tr').length <= 1) {
        // The last item in a module section was deleted or the add operation was canceled

        // The module section's h4 element contains the correct verbose name for each module
        var parent_name = target.find('h4').text();

        // Remove the empty section
        target.remove();

        // Replace the button within the moduleBank table and display the moduleBank
        $("#moduleBank table").append(
            "<tr class='profile_section'><td><a id='"+module+"-section' href=''>"+parent_name+"</a></td></tr>"
        );
        $("#moduleBank").show();
    }
}

function datepicker() {
    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd"});
    });
};
