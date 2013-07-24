$(document).ready(function() {
    /*
    Targets event fired when "Search Name" column is clicked
    */
    $('.view_search').click(function(e) {
        // Only redirect when at mobile resolution (<= 500px)
        if ($(window).width() <= 500) {
            // id is formatted saved-search-[id]
            var id = $(e.target).parent().attr('id').split('-')[2];
            window.location = id;
        }
    });
});
