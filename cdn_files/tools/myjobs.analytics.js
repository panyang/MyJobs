var _paq = _paq || [];
(function() { var u = (("https:" == document.location.protocol) ? "https://secure.my.jobs/analytics/track" : "http://secure.my.jobs/analytics/track")
    _paq.push(['setTrackerUrl', u]);
    _paq.push(['setDocumentTitle',
               document.domain + '/' + document.title]);
    $('#savedsearch_button').click(function() {
        _paq.push(['trackGoal', 'save search']);
    });
    $('[id^=direct_applyButton]').click(function() {
        _paq.push(['setCustomVariable', 1, 'url',
                   $(this).children('a')[0].href])
        _paq.push(['trackGoal', 'apply']);
    });
    $('[class*=at16nc]').click(function() {
        var text = $(this).html();
        if (text.indexOf('More...') == 0) {
            _paq.push(['setCustomVariable', 1, 'share', 'Other'])
        } else if (text.indexOf('Settings...') == 0) {
            return;
        } else {
            _paq.push(['setCustomVariable', 1, 'share', $(this).html()]);
        }
        _paq.push(['trackGoal', 'share']);
    });
    $('[class*=at15nc]').click(function() {
        var text = $(this).children('span')[0];
        if (text !== undefined) {
            text = $(text).html();
            if (text !== null && text.indexOf('Share on ') == 0) {
                _paq.push(['setCustomVariable', 1, 'share', text.substr(9)]);
                _paq.push(['trackGoal', 'share']);
            }
        }
    })
    _paq.push(['enableLinkTracking'])
    _paq.push(['trackPageView']);
    var d = document,
        g = d.createElement('script'),
        s = d.getElementsByTagName('script')[0];
    g.type='text/javascript';
    g.defer=true;
    g.async=true;
    g.src="//d2e48ltfsb5exy.cloudfront.net/myjobs/tools/piwik.js";
    s.parentNode.insertBefore(g,s);
})();
