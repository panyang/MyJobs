$('#twitter').live('click',function() {
    q=location.href;
    window.open('/auth/twitter/?&url='+encodeURIComponent(q),
                'Share this on Twitter','toolbar=no,width=660,height=455');
});
$('#facebook').live('click',function() {
    q=location.href;
    window.open('/auth/facebook/?&url='+encodeURIComponent(q),
                'Share this on Facebook','toolbar=no,width=660,height=455');
});
$('#linkedin').live('click',function() {
    q=location.href;
    window.open('/auth/linkedin/?&url='+encodeURIComponent(q),
                'Share this on Twitter','toolbar=no,width=660,height=455');
});
