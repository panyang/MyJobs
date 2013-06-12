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
                    if (data == "success") {
                        $('ul.errorlist').remove();
                        if (auto_user) {
                            window.location.href='/';
                        } else {
                            $("a[id^='account-']")
                                .removeClass("password-required");
                            $('.form-status').html('<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">&times;</button>Your information has been updated.</div>');                       }
                    } else {
                        var json = jQuery.parseJSON(data);

                        // remove color from labels of current errors
                        $('[class*=required]').prev().css('color', '#000');

                        // remove red border around past required fields
                        $('[class*=required]').children().css('border', '1px solid #CCC')

                        // remove current errors
                        $('[class*=required]').children().unwrap();

                        for (var index in json.errors) {
                            // for edit-basic, json.error name is __all__(all fields)
                            if(json.errors[index][0] == '__all__'){
                                var $error1 = $('#id_given_name');
                                var $error2 = $('#id_family_name');

                                // Wrap the error in a span (for easy css changes)
                                $error1.wrap('<span class="required" />');
                                $error2.wrap('<span class="required" />');

                                // Edits placeholder to show error, errors 
                                // thrown up by views.py
                                $error1.attr("placeholder", json.errors[index][1]);
                                $error2.attr("placeholder", json.errors[index][1]);

                                $error1.css('border', '1px solid #900');
                                $error2.css('border', '1px solid #900');

                                $error1.parent().prev().children().css('color', '#900');
                                $error2.parent().prev().children().css('color', '#900');
                            }
                            else
                            {
                                var $error = $('[id$="_'+json.errors[index][0]+'"]');
                                var $labelOfError = $error.prev();
                                // insert new errors after the relevant inputs
                                $error.wrap('<span class="required" />');
                                $error.attr("placeholder", json.errors[index][1]);
                                $error.css('border', '1px solid #900');
                                $labelOfError.css('color', '#900');
                            }
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
});
