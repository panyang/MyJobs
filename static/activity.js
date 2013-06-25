$(document).ready(function(){
		//Looks bootstrap collasping classes and changes icon to + or -
	$('[class*=details-heading]').click(function(){
			var icon = $(this).children('a').children('span').children('i');
			var item = $(this).next();
			/*
				This function is ran before 'in' gets placed so logic 
				has to be backwards.
			*/
			if(item.hasClass('in')){
				if(icon.hasClass('icon-minus')){
					icon.removeClass('icon-minus');
					icon.addClass('icon-plus');
				}
			}else{
				icon.removeClass('icon-plus');
				icon.addClass('icon-minus');
			}
	});
});