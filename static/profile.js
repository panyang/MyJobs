$(function() {
    if ($('#moduleBank').find('tr:visible').length == 0) {
        $('#moduleBank').hide();
    }
        
    var AppView = Backbone.View.extend({
        el: $("body"),

        events: {
            // targets event fired when buttons within #moduleBank are clicked
            "click [id$='section']": "editForm",

            // targets event fired when "Add Another" buttons in each module
            // section are clicked
            "click [id$='add']": "editForm",

            // targets "Edit" buttons for individual modules
            "click [id$='edit']": "editForm",

            // targets event fired when a modal is hidden
            "hidden [id$='modal']": "cancelForm",

            // targets "Save" button  in the modal window
            "click [id$='save']": "saveForm",

            // targets "Delete" button on confirmation modal
            "click [id$='delete']": "deleteItem",

            // targets country select boxes
            "change [id$='-country_code']": "getSelect",

            // targets delete buttons not on confirmation modal
            "click [id$='confirm']": "confirmDelete",

            // targets "View" button for each item
            "click [id$='view']": "viewDetails",
        },

        /*
        Returns document to the state it was in prior to opening the most 
        recent modal. Called when a modal is hidden

        :e: modal window
        */
        cancelForm: function(e) {
            e.preventDefault();

            var target = $(e.target).find('a[id$="cancel"]');

            // this file may be included in a location whose structure does not
            // support this event. If it does not, return immediately.
            try {
                // id is formatted [module_type]-[item_id]-[event]
                var module = target.attr('id').split('-')[0];
                var item_id = target.attr('id').split('-')[1];
            } catch(e) {
                return;
            }
            if (!$('[id$="modal"]:visible').length) {
                // All modals are hidden; Remove them
                $('[id$="modal"]').remove();
            }

            manageModuleDisplay(module);
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
            if (id == 'new') {
                $(e.target).parents('.profile-section').hide();
                if ($('#moduleBank').find('tr:visible').length == 0) {
                    $('#moduleBank').hide();
                }
            } else {
                // targets the table row containing the item to be edited
                item = $('#'+module+'-'+id+'-item');
            } 

            if ($('#edit_modal').length == 0) {
                $.ajax({
                    url: '/profile/form/',
                    data: {'module':module, 'id':id},
                    success: function(data) {
                        $('#moduleColumn').append(data);

                        $('#edit_modal').modal();
                        datepicker();

                        $('[id$="-country_sub_division_code"]').hide();
                        $('label[for$="-country_sub_division_code"]').hide();
                        $('[id$="-country_code"]').change();
                    }
                });            
            } else {
                $('#edit_modal').modal();
            }
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

            console.log(module);
            console.log(item_id);
            console.log(form);
            console.log(csrf_token);

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
                    console.log(data);
                    if (data.indexOf('<td') >= 0) {
                        // form was valid
                        if ($('#'+module+'_items').length < 1) {
                            $('#moduleColumn').append(data);
                        } else {
                            $('#'+module+'-'+item_id+'-item').remove();
                            if (first_instance) {
                                $('#'+module+'_items').children('h4').after(
                                    '<table class="table table-bordered table-striped"></table>'
                                );
                                table = $('#'+module+'_items').children('table');
                                table.append(data);
                            }
                            else {
                                table.children("tbody").append(data);
                            }
                        }
                        $('[id$="modal"]').modal('hide');
                    } else {
                        // form was a json-encoded list of errors and error messages
                        var json = jQuery.parseJSON(data);

                        // remove color from labels of current errors
                        $('[class*=required]').parent().prev().css('color', '#000');

                        // remove current errors
                        $('[class*=required]').children().unwrap();

                        for (var index in json.errors) {
                            var $error = $('[id$="-'+json.errors[index][0]+'"]');
                            var $labelOfError = $error.parent().prev();
                            // insert new errors after the relevant inputs
                            $error.wrap('<span class="required" />');
                            $error.attr("placeholder",json.errors[index][1]);
                            $labelOfError.css('color', '#900');

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
                    $('[id$="modal"]').modal('hide').remove();
                    item.remove();
                    manageModuleDisplay(module);
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

            $.ajax({
                url: '/profile/details/',
                data: {'module': module, 'id': id},
                success: function(data) {
                    $(e.target).parents('table').after(data);
                    var target = $('#detail_modal');
                    target.modal();
                }
            });
        },

        /*
        Shows a confirmation message to determine if user really wants
        to delete the specified item

        :e: "Delete" button within item details modal
        */
        confirmDelete: function(e) {
            e.preventDefault();
            $('#confirm_modal').modal();
        },
    });

    var App = new AppView;
});

function manageModuleDisplay(module) {
    var target = $('#'+module+'_items');
    if (target.find('table tr').length <= 1) {
        // The last item in a module section was deleted or the add operation was canceled

        // Remove the empty section
        target.remove();

        // Re-show the button within the moduleBank table and display the moduleBank
        $('#'+module+'-new-section').parents('.profile-section').show();
        $("#moduleBank").show();
    }
}

function datepicker() {
    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd",
                                             constrainInput: false});
    });
};
