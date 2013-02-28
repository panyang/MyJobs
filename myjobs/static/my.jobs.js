/******
Document Level Actions
*******/
$(document).ready(function(){
    var offset = 0;
    
    /*Explicit control of main menu, primarily for mobile but also provides
    non hover and cover option if that becomes an issue.*/
    $("#nav .main-nav").click(function(){
        $("#nav").toggleClass("active");
        return false;
    });
    $("#pop-menu").mouseleave(function(){
        $("#nav").removeClass("active");
    });

    $(window).scroll(function(){
        if ($(window).scrollTop() == $(document).height() - $(window).height())
        {
            offset += 20;
            $.ajax({
                url: "/saved-search/more-results",
                data: { 'offset': offset,
                        'frequency': frequency,
                        'feed': feed
                      },
                success: function(data) {
                    $('.feed-page').append(data);
                }
            });
        }
    });

    if ($("#digest_error .errorlist li").text().length == 0 && $('#id_digest_active').prop('checked') == false) {
        $("#id_digest_email").hide();
        $("label[for=id_digest_email]").hide();
        $("#digest_submit").hide();
    }
    
    $('#id_digest_active').click(function() {
        if( $(this).is(':checked')) {
            $("#id_digest_email").show();
            $("label[for=id_digest_email]").show();
            $("#digest_submit").show();
        } else {
            $("#id_digest_email").hide();
            $("label[for=id_digest_email]").hide();
            $("#digest_submit").hide();
        }
    }); 
});

/*Combobox Widget. Based loosely on the jQuery UI example*/
(function($){$.widget( "ui.makeCombobox",{
    _create: function(){
        parent = this.element;
        selected = parent.children( ":selected" )
        parent_id = parent.attr("id");
        parent_label = $("label[for="+parent_id+"]")
        parent_id_orig = parent_id+"_orig";
        parent.attr("id",parent_id_orig)
        parent.hide();
        new_ac = $("<input>")
            .attr("id",parent_id)                                           
            .attr("type","text")
            .attr("value",selected.html())
            .attr("placeholder",parent_label.html())
            .addClass("comboboxWidget")
            .addClass(parent.attr("class"))            
            .insertBefore(parent)
            .autocomplete({
                source: function(req,resp){
                    /****
                    Dynamically build the AC list from parent select list.
                    Doing it this way allows for the AC to pick up changes
                    in the option list made by ajax.
                    ****/
                    dict = [];
                    source = $("#"+this.element.attr("id")+"_orig").children("option");
                    for(i=0;i<source.length;i++){
                        label = source[i].innerHTML;
                        value = source[i].value;
                        if(source[i].value != "" &&
                           label.toLowerCase().indexOf(req.term.toLowerCase())!=-1){
                                dict.push({"label":label,"value":label});                            
                        }
                    }
                    resp(dict);
                },
                minLength: 0,
                select: function(event,ui){
                    /****
                    On select, get the value of the field, and check if
                    the field has a dependent region list. If so, get that
                    listing from jsonp and populate the select list with the
                    the new data.                        
                    ****/
                    my_parent = $("#"+this.id+"_orig");
                    if(my_parent.hasClass("hasRegions")){
                        /****
                        This is logic specific to the region select list
                        when the combo box is being applied to a country
                        select list that also has a region list assigned
                        to it. The majority of the time, this will be due
                        to the use of the {% country_region_select %}
                        template tag.
                        ****/
                        target_id = my_parent.attr("data-childlistid");
                        orig_options = my_parent.children("option")
                        val_to_get = "";
                        for(opt=0; opt < orig_options.length; opt++){
                            if (ui.item.label==$(orig_options[opt]).html()){
                                val_to_get = $(orig_options[opt]).val()
                            }
                        }       
                        // build the url for the jsonp ajax call
                        region_url = "http://js.nlx.org/myjobs/data/";
                        region_url+= val_to_get.toLowerCase();
                        region_url+= "_regions.jsonp";
                        //store label visibility state
                        label_visibility = false;
                        if($("label[for="+target_id+"]").is(":visible")){
                            label_visibility = true;
                        }
                        //temp hide the region select in case of 404 on the json                        
                        $("label[for="+target_id+"]").hide()
                        $("#"+target_id+" + a").hide()
                        $("#"+target_id+"").hide()
                        $("#"+target_id+"_orig").val("none")
                        //make the ajax call for region data
                         $.ajax({
                            url: region_url,
                            dataType: "jsonp",
                            data: {},
                            // the jsonp files are static, so the callback
                            // must be set manually, not by jQuery
                            jsonpCallback: "returnRegionData",
                            success: function(data){
                                // replace the <option>s for the parent.
                                // the widget will take note and update
                                // itself
                                var opts = ""
                                for(var i in data.regions){
                                    item = data.regions[i]
                                    opts_attrs = "value='"+item.code+"'";
                                    if(item.code.toLowerCase()==data.default_option.toLowerCase()){
                                        opts_attrs += " SELECTED";
                                    }
                                    opts+="<option "+opts_attrs+">";
                                    opts+=item.name+"</option>";
                                }
                                if(typeof(data.friendly_label)!="undefined"){
                                    label = data.friendly_label;
                                }else{
                                    label = "Region";
                                }
                                if(opts!=""){
                                    $("#"+target_id+"_orig").html(opts);
                                    // turn on the region widget
                                    $("label[for="+target_id+"]").html(label)
                                    if(label_visibility){
                                        $("label[for="+target_id+"]").show()
                                    }
                                    $("#"+target_id+" + a").show()
                                    $("#"+target_id+"").show()
                                    //set widget default value
                                    $("#"+target_id+"").val(
                                        $("#"+target_id+"_orig")
                                        .children(":selected").html()
                                        );
                                }
                            }
                        });                         
                    }
                },
                change: function(){
                    /*****
                    Link the original select box to the dynamic AC field
                    *****/
                    orig_options = $("#"+this.id+"_orig").children("option")
                    ac_field = this;
                    val_to_select = "";
                    for(opt=0; opt < orig_options.length; opt++){
                        if (ac_field.value==$(orig_options[opt]).html()){
                            val_to_select = $(orig_options[opt]).val()
                        }
                    }
                    my_parent = $("#"+this.id+"_orig");
                    my_parent.val(val_to_select);
                }
            });
        $("<a>")
            .attr( "title", "Show All Items")
            .attr( "data-for",parent_id)
            .insertAfter(new_ac)
            .button({
                icons: {
                    primary: "ui-icon-triangle-1-s"
                },
                text: false
            })
            .addClass( "ui-corner-right ui-combobox-toggle" )
            .click(function() {
                // close if already visible
                if ( new_ac.autocomplete( "widget" ).is( ":visible" ) ) {
                    new_ac.autocomplete( "close" );
                    return;
                }

                // work around a bug (likely same cause as #5265)
                $( this ).blur();

                // pass empty string as value to search for, displaying all results
                target = $(this).attr("data-for");
                $("#"+target).autocomplete( "search", "" );
                $("#"+target).focus();
            });
        itemCount = $("#"+parent_id_orig).children("option")
        //If there are no options for this element, hide it.
        if(typeof(itemCount[1])=="undefined" || itemCount[1].value == ""){
            $("label[for="+parent_id+"]").hide();
            $("#"+parent_id+" + a").hide();
            $("#"+parent_id+"").hide();
            $("#"+parent_id+"_orig").val("none");
        }
    },
    destroy: function() {
        this.element.show();
        $.Widget.prototype.destroy.call( this );
    }
})})( jQuery )
