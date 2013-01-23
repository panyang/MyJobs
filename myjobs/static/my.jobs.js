/******
Document Level Actions
*******/
$(document).ready(function(){
    $("select").makeCombobox();
});
/******
My.jobs Share window functions. Assigns click events and builds share window. 
*******/
$('#twitter').live('click',function() {        
    q=location.href;
    share_url = '/auth/twitter/?&url='+encodeURIComponent(q);
    openShareWindow(share_url,"Twitter");
});
$('#facebook').live('click',function() {
    q=location.href;
    share_url = '/auth/facebook/?&url='+encodeURIComponent(q);
    openShareWindow(share_url,"Twitter");
});
$('#linkedin').live('click',function() {
    q=location.href;
    share_url = '/auth/linkedin/?&url='+encodeURIComponent(q);
    openShareWindow(share_url,"LinkedIn");
});
$(document).ready(function(){
    console.log("ready");
    $(".topbar .main-nav").click(function(){
        $("#nav").toggleClass("active");
        return false;
    });
});
function openShareWindow(url,name){
    /*
    Opens a new window using OAuth to share content.
    
    Inputs:
        :url:   The share url to use
        :name:  The name of the social network
    
    Returns:
        None - opens a new window.
    
    */
    title = 'Share this on '+name;
    atts = 'toolbar=no,width=568,height=360';
    share_window = window.open(url, title,atts);
}
function repopulateSelectField(field_id, new_data, use_combobox){
    option_string = "";
    if(typeof(use_combobox=="undefined")){use_combobox=true;}
    for(i=0;i<new_data.length;i++){
        option_string+="<option value='"+new_data[i].key+"'>";
        option_string+=new_data[i].value+"</option>";
    }
    $("#"+field_id).html(option_string);
    //$("#"+field_id+" + .ui-combobox").remove();
    $("#"+field_id).combobox();
    console.log(use_combobox)
}

/*Combobox Widget. Based loosely on the jQuery UI example*/
(function($){
    $.widget( "ui.makeCombobox",{
        _create: function(){
            parent = this.element;
            selected = parent.children( ":selected" )
            parent_id = parent.attr("id");
            parent_id_orig = parent_id+"_orig";
            parent.attr("id",parent_id_orig)
            parent.hide();
            new_ac = $("<input>")
                .attr("id",parent_id)
                .attr("type","text")
                .attr("value",selected.html())
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
                            if(source[i].value != ""){
                            // if the search phrase is in the label
                                if(label.toLowerCase().indexOf(req.term.toLowerCase())!=-1){
                                    dict.push({"label":label,"value":label});
                                }
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
                            orig_options = my_parent.children("option")
                            val_to_get = "";
                            for(opt=0; opt < orig_options.length; opt++){
                                if (ui.item.label==$(orig_options[opt]).html()){
                                    val_to_get = $(orig_options[opt]).val()
                                }
                            }       
                            // build the url for the jsonp ajax call
                            region_url = "http://js.nlx.org/myjobsdata/";
                            region_url+= val_to_get.toLowerCase();
                            region_url+= "_regions.jsonp";
                            //temp hide the region select in case of 404
                            $("#region_selection + a").hide()
                            $("#region_selection").hide()
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
                                    for(var key in data){
                                        value = data[key];
                                        opts+="<option value="+key+">";
                                        opts+=value+"</option>";
                                    }                                    
                                    if(opts!=""){
                                        $("#region_selection_orig").html(opts);
                                        // turn on the region widget
                                        $("#region_selection + a").show()
                                        $("#region_selection").show()
                                        //set widget default value
                                        $("#region_selection").val(
                                            $("#region_selection_orig")
                                            .children(":selected").html()
                                            );
                                    }
                                },
                                error:function(x,str,err){
                                    console.log("error");
                                    $("#region_selection + a").hide()
                                    $("#region_selection").hide()
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
                        //TODO make sure this is getting set right after changes to select
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
        },
        destroy: function() {
            this.element.show();
            $.Widget.prototype.destroy.call( this );
        }
    })
})( jQuery )
