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
function openShareWindow(url,name){    
    window.open(url, 'Share this on '+name,'toolbar=no,width=568,height=360');
}
