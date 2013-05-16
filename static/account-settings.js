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
            var section_name = $(e.target).attr('id').split('-')[1];
            $.ajax({
                type: "POST",
                data: $(e.target).serialize(),
                url: "/edit/" + section_name,
                success: function(data) {
                    if (data == "success") {
                        $('.form-status').html('<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">&times;</button>Your information has been updated.</div>');
                    } else {
                        $('div.account-settings').html(data);
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
