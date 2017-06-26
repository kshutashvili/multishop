$(document).ready(function(){

$(function () {
	//script for popups
	
	$('.show_popup').click(function () {
		$('div.'+$(this).attr("data-rel")).fadeIn(500);
		//$("body").append("<div class='shadow'></div>");
		$('.shadow').show().css({'filter' : 'alpha(opacity=80)'});
		return false;				
	});	
	$('a.close').click(function () {
		$(this).parent().fadeOut(100);
		//$('.shadow').remove('.shadow');
		$('.shadow').hide();
		if ($('.headhesive').css('display') == 'none') {
			$('.headhesive').show();
		}
		return false;
	});
	$('.close_modal').click(function () {
		$(this).parent().parent().fadeOut(100);
		return false;
	});
	$('.close_modal_second').click(function () {
		$(this).parent().parent().parent().fadeOut(100);
		return false;
	});

});
});