$(document).ready(function() {
    var offset = 0;
    $(window).scroll(function(){
        if ($(window).scrollTop() == $(document).height() - $(window).height())
        {
            offset += 20;
            $.ajax({
                url: "/" + user_email + "/saved-search/more-results",
                data: { 'offset': offset,
                        'frequency': frequency,
                        'feed': feed,
                        'sort_by': sort_by
                      },
                success: function(data) {
                    $('#saved-search-listing-table tbody').append(data);
                }
            });
        }
    });
});
