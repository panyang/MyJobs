$(document).ready(function(){
	$('.collapse').collapse().on('hidden',function(){
		if(this.id){
			localStorage[this.id] = "true";
		}
	}).on('shown', function(){
		if(this.id){
			localStorage.removeItem(this.id);
		}
	}).each(function(){
		var icon = $(this).prev().children('a').children('span').children('i');
		if (this.id && localStorage[this.id] === 'true'){
			$(this).collapse('hide');
			icon.removeClass('icon-minus');
			icon.addClass('icon-plus');
		}else{
			icon.removeClass('icon-plus');
			icon.addClass('icon-minus');
		}
	});
	$('#candidate-page-mobile-view').each(function(){
		if (this.id && localStorage[this.id] === "true"){
			$(this).addClass('show-activity');
			$(this).removeClass('show-details');
		}else{
			$(this).addClass('show-details');
			$(this).removeClass('show-activity');
		}
	});
	//when heading get clicked. Looks bootstrap collasping classes and changes icon to + or -
	$('[class*=details-heading]').click(function(){
		var icon = $(this).children('a').children('span').children('i');
		var item = $(this).next();
		item.collapse().on('shown',function(){
			icon.removeClass('icon-plus');
			icon.addClass('icon-minus');
		}).on('hidden',function(){
			icon.removeClass('icon-minus');
			icon.addClass('icon-plus');
		});
	});
	$('[id$=detail-toggle]').click(function(){
		container = $(this).parent().parent();
		container.removeClass('show-activity');
		container.addClass('show-details');
	});
	$('[id$=activity-toggle]').click(function(){
		container = $(this).parent().parent();
		container.removeClass('show-details');
		container.addClass('show-activity');
	});
});