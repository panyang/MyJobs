var _paq = _paq || [];
(function() { var u = (("https:" == document.location.protocol) ? "https://secure.my.jobs/analytics/track" : "http://secure.my.jobs/analytics/track")
    _paq.push(['setTrackerUrl', u]);
    _paq.push(['setDocumentTitle',
               document.domain + '/' + document.title]);
    $('#savedsearch_button').click(function() {
        _paq.push(['trackGoal', 'save search']);
    });
    $('[id^=direct_applyButton]').click(function() {
        _paq.push(['setCustomVariable', 1, 'url', $(this).children('a')[0].href])
        _paq.push(['trackGoal', 'apply']);
    });
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
