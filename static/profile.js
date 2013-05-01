$(function() {
    var AppView = Backbone.View.extend({
        el: $(".row"),

        events: {
            // targets event fired when buttons within #moduleBank are clicked
            "click [id$='section']": "addSection",

            // targets event fired when "Add Another" buttons in each module
            // section are clicked
            "click [id$='add']": "editForm",

            // targets "Edit" buttons for individual modules
            "click [id$='edit']": "editForm",

            // targets event fired when "Cancel" or "x" buttons within modals
            // are clicked
            "click [id$='cancel']": "cancelForm",

            // targets "Save" button  in the modal window
            "click [id$='save']": "saveForm",

            // targets "Delete" button on confirmation modal
            "click [id$='delete']": "deleteItem",

            // targets country select boxes
            "change [id$='-country_code']": "getSelect",

            // targets "Delete" button on add/edit modal
            "click [id$='confirm']": "confirmDelete",

            // targets "View" button for each item
            "click [id$='view']": "viewDetails",
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
        Returns document to the state it was in prior to opening the most 
        recent modal. Called on "Cancel" button click or closure of the
        modal window

        :e: cancel buttons within modal window
        */
        cancelForm: function(e) {
            e.preventDefault();

            // e.target may be either the cancel button or the x button;
            // We need the cancel button
            var target = $(e.target).parents('[id$="modal"]')
                .find('a[id$="cancel"]');

            // id is formatted [module_type]-[item_id]-[event]
            var module = target.attr('id').split('-')[0];
            var item_id = target.attr('id').split('-')[1];

            var modal = target.parents('.modal')
            if (modal.attr('data-parent') !== undefined) {
                // The modal being closed was opened by another modal;
                // It should be hidden and its parent modal should be shown
                modal.modal('hide');
                parent_modal = $('#'+modal.attr('data-parent'));
                modal.removeAttr('data-parent');
                parent_modal.modal({'backdrop':'static','keyboard':false});
            } else {
                // Upon closing certain modal windows, all modals should be
                // removed from the document
                $('[id$="modal"]').modal('hide').remove();
            }

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
                item = $('#'+module+'-'+id+'-item');
            }

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
                    $('#edit_modal').modal({'backdrop':'static','keyboard':false});
                    datepicker();

                    $('[id$="-country_sub_division_code"]').hide();
                    $('label[for$="-country_sub_division_code"]').hide();
                    $('[id$="-country_code"]').change();
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
            var serialized_data = form.serialize();
            serialized_data += '&module=' + module + '&id=' + item_id +
                               '&first_instance=' + first_instance +
                               '&csrfmiddlewaretoken=' + csrf_token;
            $.ajax({
                type: 'POST',
                url: '/profile/form/',
                data: serialized_data,
                success: function(data) {
                    if (data.indexOf('<td') >= 0) {
                        // form was valid; data should be appended to the table
                        if (first_instance) {
                            $('#'+module+'_items').children('h4').after(
                                '<table class="table table-bordered table-striped"></table>'
                            );
                            table = $('#'+module+'_items').children('table')
                        }
                        table.children("tbody").append(data);
                        $('#'+module+'-'+item_id+'-item').remove();
                        $('[id$="modal"]').modal('hide');
                        $('[id$="modal"]').remove();
                        $('#'+module+'_items').show();
                    } else {
                        // form was a json-encoded list of errors and error messages
                        var json = jQuery.parseJSON(data);

                        // remove current errors
                        $('[class*=label-important]').remove();
                        for (var index in json.errors) {
                            // insert new errors after the relevant inputs
                            $('[id$="-'+json.errors[index][0]+'"]').after(
                                '<span class="label label-important">'+
                                json.errors[index][1]+'</span>');
                        }
                    }
                }
            });            
        },

        /*
        Deletes the specified item

        :e: "Delete" button within the delete confirmation modal
        */
        deleteItem: function(e) {
            e.preventDefault();
            csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
            var csrf_token = "";
            if(typeof(csrf_token_tag)!='undefined'){
                csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            }

            // id is formatted [module_type]-[item_id]-delete
            var module = $(e.target).attr('id').split("-")[0];
            var id = $(e.target).attr('id').split("-")[1];

            // targets the table row containing the item to be deleted
            var item = $('#'+module+'-'+id+'-item');

            $.ajax({
                type: 'POST',
                url: '/profile/delete/',
                data: {'module':module, 'id':id, csrfmiddlewaretoken: csrf_token},
                success: function(data) {
                    $('#edit_modal').modal('hide');
                    $('#edit_modal').remove();
                    item.remove();
                    manageModuleDisplay(module);
                    $('[id$="modal"]').modal('hide').remove();
                }
            });
        },

        /*
        Gets a list of regions, if any, for a specific country
        and formats them in a select menu.
        */
        getSelect: function() {
            var country = $('[id$="-country_code"]').val();
            var elem = $('[id$="-country_sub_division_code"]');
            var id = elem.attr('id');
            var name = elem.attr('name');
            var old_val = elem.val();
            if (!old_val) {
                old_val = "";
            }

            var region_url = "http://js.nlx.org/myjobs/data/";
            region_url += country.toLowerCase();
            region_url += "_regions.jsonp";

            // Hide region selector and its label in case we receive a 404
            $("label[for='"+id+"']").hide();
            elem.hide();

            $.ajax({
                url: region_url,
                dataType: "jsonp",
                data: {},
                jsonpCallback: "returnRegionData",
                success: function(data) {
                    var opts = "";
                    for (var i in data.regions) {
                        item = data.regions[i]
                        opts_attrs = "value='"+item.code+"'";
                        if (item.code.toLowerCase() == old_val.toLowerCase() ||
                            item.code.toLowerCase() == data.default_option.toLowerCase()) {
                            // This is either the default for a new profile unit
                            // or the value of a unit being edited
                            opts_attrs += " SELECTED";
                        }
                        opts += "<option "+opts_attrs+">";
                        opts += item.name+"</option>";
                    }
                    if (typeof(data.friendly_label) != "undefined") {
                        label = data.friendly_label;
                    } else {
                        label = "Region";
                    }
                    if (opts != "") {
                        select = $("<select />", {
                            id: id,
                            name: name,
                        });
                        select.html(opts);
                        elem.after(select);
                        elem.remove();
                        $("label[for="+id+"]").html(label)
                        $("label[for="+id+"]").show();
                    }
                },
            });
        },

        viewDetails: function(e) {
            e.preventDefault();

            // id is formatted [module_type]-[item_id]-view
            var module = $(e.target).attr('id').split('-')[0];
            var id = $(e.target).attr('id').split('-')[1];
            console.log(id)
            console.log($(e.target).attr('id'))

            var target = '#'+module+'-'+id+'-detail_modal';
            console.log($(target).length)
            if ($(target).length == 1) {
                $(target).modal({'backdrop':'static','keyboard':false});
            } else {
                $.ajax({
                    url: '/profile/details/',
                    data: {'module': module, 'id': id},
                    success: function(data) {
                        $(e.target).parents('table').after(data);
                        console.log($(target).length)
                        $(target).modal({'backdrop':'static','keyboard':false});
                    }
                });
            }
        },

        /*
        Shows a confirmation message to determine if user really wants
        to delete the specified item

        :e: "Delete" button within item details modal
        */
        confirmDelete: function(e) {
            e.preventDefault();
            var parent_modal = $(e.target).parents('[id$="modal"]')
            parent_modal.modal('hide');
            resize_modal('#confirm_modal');
            $('#confirm_modal').attr('data-parent', parent_modal.attr('id'));
            $('#confirm_modal').modal({'backdrop':'static','keyboard':false});
        },
    });

    var App = new AppView;

    $(window).on('resize', function() {
        resize_modal('#confirm_modal');
        resize_modal('#edit_modal');
    });
});

function manageModuleDisplay(module) {
    var target = $('#'+module+'_items');
    if (target.find('table tr').length <= 1) {
        // The last item in a module section was deleted or the add operation was canceled

        var verbose_name = $('#'+module+'-verbose').text();

        // Remove the empty section
        target.remove();

        // Replace the button within the moduleBank table and display the moduleBank
        $("#moduleBank table").append(
            "<tr class='profile_section'><td><a id='"+module+"-section' href=''>"+verbose_name+"</a></td></tr>"
        );
        $("#moduleBank").show();
    }
}

function datepicker() {
    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd"});
    });
};
