$(document).ready(function() {
    $(window).on("resize", function(e) {
        if ($(window).width() < 500) {
            $('div.settings-nav').show();
            $('div.account-settings').hide();
        } else {
            $('div.settings-nav').show();
            $('div.account-settings').show();
        }
    });
});

$(function() {
    var AppView = Backbone.View.extend({
        el: $("body"),
        events: {
            "click [id^='account-']": "showSection",
            "submit form": "saveForm",
            "click [id^='show-captcha-modal']": "captchaModal",
        },
        
        showSection: function(e) {
            e.preventDefault();
            $('div.account-settings').html("");            
            try {
                var section_name = $(e.target).parents('a').attr('id').split('-')[1];
            } catch(err) {
                var section_name = $(e.target).attr('id').split('-')[1];
            }
            $.ajax({
                url: "/edit/" + section_name,
                success: function(data) {
                    $('div.account-settings').html(data);
                }
            });
        },

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

            // grabs closest form to the button, good since 
            // this function is used for different forms.
            var form = $(e.target).closest("form");

            // protection from cross site requests
            csrf_token_tag = document.getElementsByName('csrfmiddlewaretoken')[0];
            var csrf_token = "";
            if(typeof(csrf_token_tag)!='undefined'){
                csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            }
            first_instance=0;
            var section_name = $(e.target).attr('id').split('-')[1];
            var serialized_data = form.serialize();
            serialized_data += '&module=' + module + '&id=' + item_id +
                               '&first_instance=' + first_instance +
                               '&csrfmiddlewaretoken=' + csrf_token;
            $.ajax({
                type: "POST",
                data: serialized_data,
                url: "/edit/" + section_name,
                success: function(data) {
                    console.log(data);
                    if (data == "success") {
                        // Remove all required field changes, if any
                        removeRequiredChanges();
                        if (auto_user) {
                            window.location.href='/';
                        } else {
                            $("a[id^='account-']")
                                .removeClass("password-required");
                            $('.form-status').html('<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">&times;</button>Your information has been updated.</div>');                       }
                    } else {
                        var json = jQuery.parseJSON(data);

                        // if there is a previous alert-success present
                        // remove alert-success
                        if ($('.form-status').children().length > 0){
                            $('.form-status').empty();
                        }
                        // Remove all required field changes, if any
                        removeRequiredChanges();
                        for (var index in json.errors) {
                            var $error = $('[id$="_'+json.errors[index][0]+'"]');
                            var $labelOfError = $error.prev();
                            // insert new errors after the relevant inputs
                            $error.wrap('<span class="required" />');
                            // if on password form
                            if(item_id == "password"){
                                $error.val(''); 
                            }
                            $error.attr("placeholder", json.errors[index][1]);
                            $error.css('border', '1px solid #900');
                            $labelOfError.css('color', '#900');
                        }
                    }
                }
            });
                  
        },
        
        captchaModal: function(e) {
            e.preventDefault();
            $("#captcha_modal").modal();
        },

    });

    var App = new AppView;

    function removeRequiredChanges(){
        // remove color from labels of current errors
        $('[class*=required]').prev().css('color', '#000');

        // remove red border around past required fields
        $('[class*=required]').children().css('border', '1px solid #CCC');

        // remove current errors
        $('[class*=required]').children().unwrap();
    }
});
