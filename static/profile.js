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

            // targets email reactivation link in SecondaryEmail window
            "click [id$='updateEmail']": "updateEmail",

            // targets "Delete" button on confirmation modal
            "click [id$='delete']": "deleteItem",

            // targets delete buttons not on confirmation modal
            "click [id$='confirm']": "confirmDelete",

            // targets "View" button for each item
            "click [id$='view']": "viewDetails",

            // targets calendar buttons for each DateField
            "click [class$='calendar']": "datepickerButton",

            // targets "I still work here" checkbox in Employment History
            "click [id='id_employmenthistory-current_indicator']": "hideEndDate",
        },

        /*
        Hides the end date if the "I still work here" checkbox is checked
        */
        hideEndDate: function() {
            if(($("[id='id_employmenthistory-current_indicator']").is(":checked"))) {
                $("[id='id_employmenthistory-end_date']").hide();
                $("[for='id_employmenthistory-end_date']").hide();
            }
            else {
                $("[id='id_employmenthistory-end_date']").show();
                $("[for='id_employmenthistory-end_date']").show();
            }
        },

        /*
        Shows the datepicker that is already connected DateField in profile modals
        */
        datepickerButton: function(e) {
            e.stopPropagation();    
            e.preventDefault();
            that = $(e.target).parents('.input-append');
            if ($('#ui-datepicker-div').css("display") == "block") {
                that.find('[id$="date"]').datepicker('hide');
            }
            else {
                that.find('[id$="date"]').datepicker('show');
            }
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
                        // Prevents end date from showing up if "I still work here" is checked
                        if(($("[id='id_employmenthistory-current_indicator']").is(":checked"))) {
                            $("[id='id_employmenthistory-end_date']").hide();
                            $("[for='id_employmenthistory-end_date']").hide();
                        }
                        $('#edit_modal').modal();
                        add_date_button($('#edit_modal'));
                        $('input[id$="date"]').datepicker({dateFormat: window.dateFormat,
                                                           constrainInput: false});
                    }
                });            
            } else {
                $('#edit_modal').modal();
            }
        },

        /*
        Resends activation link

        :e: "Resend my activation email" link within SecondaryEmail modal
        */
        updateEmail: function(e) {
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
                               '&csrfmiddlewaretoken=' + csrf_token + '&action=updateEmail';
            $.ajax({
                type: 'POST',
                url: '/profile/form/',
                data: serialized_data,
                success: function(data) {
                     $(".modal-body").prepend("<div class='alert alert-success'>Activation email resent to " + $("[name='email']").val() + "</div>");
                }
            });
        },


        /*
        Saves both new and edited modules

        :e: "Save" button within a modal
        */
        saveForm: function(e) {
            /*  
            TODO: Some of the initializing can be refactored 
            (i.e. module, item_id, csrf_token, and serialized_data)
            among some .js files; account-settings and profile 
            */

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

                        if($.browser.msie){
                            $('[class*=msieError]').remove()
                        }

                        for (var index in json.errors) {
                            var $error = $('[id$="-'+json.errors[index][0]+'"]');
                            var $labelOfError = $error.parent().prev();
                            // insert new errors after the relevant inputs
                            $error.wrap('<span class="required" />');
                            if(!($.browser.msie)){
                                $error.attr("placeholder",json.errors[index][1]);
                            }else{
                                field = $error.parent().parent().prev();
                                field.before("<div class='msieError'><i>" + json.errors[index][1] + "</i></div>");
                            }
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

function datepickerFunction() {
    $(function() {
        $( "input[id$='date']" ).datepicker({dateFormat: "yy-mm-dd",
                                             constrainInput: false});
    });
};

/*
Adds a button to the right (after) of a field that has date 
somewhere in it's ID.

.icon-search is a bootstrap function that searches a large 'sprite'
and puts up css for backposition. Called glyphicons.
*/
function add_date_button(modal) {
    modal.find('[id$="date"]').parent().addClass('input-append');
    modal.find('[id$="date"]').after('<span class="btn add-on calendar"><i class="icon-search icon-calendar"></i></span>');
}

$(document).ready(function() {
    if($(window).width() >= 501) {
        // This function will be executed when the user scrolls the page.
        $(window).scroll(function(e) {
                // Get the position of the location where the scroller starts.
                var scroller_anchor;
                try {
                    scroller_anchor = $(".scroller_anchor").offset().top;
                } catch(e) {
                    scroller_anchor = 0;
                }
     
                // Check if the user has scrolled and the current position is after the scroller start location and if its not already fixed at the top 
                if ($(this).scrollTop() >= scroller_anchor && $('#moduleBank').css('position') != 'fixed') 
                {    // Change the CSS of the scroller to hilight it and fix it at the top of the screen.
                    $('#moduleBank').css({
                            'width': '276px',
                            'position': 'fixed',
                            'top': '10px'
                });
                // Changing the height of the scroller anchor to that of scroller so that there is no change in the overall height of the page.
                $('.scroller_anchor').css('height', '50px');
                } 
                else if ($(this).scrollTop() < scroller_anchor && $('#moduleBank').css('position') != 'relative') 
                {    // If the user has scrolled back to the location above the scroller anchor place it back into the content.
         
                    // Change the height of the scroller anchor to 0 and now we will be adding the scroller back to the content.
                    $('.scroller_anchor').css('height', '0px');
         
                    // Change the CSS and put it back to its original position.
                    $('#moduleBank').css({
                            'width': 'auto',
                            'top': '0px',
                            'position': 'relative'
                });
                }
        });
    }
});


