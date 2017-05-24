$(document).ready(function(){

$(function () {
	//script for popups
	
	$('.show_popup').click(function () {
		$('div.'+$(this).attr("rel")).fadeIn(500);
		$("body").append("<div id='overlay'></div>");
		$('#overlay').show().css({'filter' : 'alpha(opacity=80)'});
		return false;				
	});	
	$('a.close').click(function () {
		$(this).parent().fadeOut(100);
		$('#overlay').remove('#overlay');
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