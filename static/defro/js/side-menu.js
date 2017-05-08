var timeout;

$('.dropdown').hover(function () {
    $(this).addClass('open');

}, function () {
    $(this).removeClass('open');

});

$('a.dropdown-toggle').click(function () {
    location.href = $(this).attr('href');
});

$('.left_side').hover(function () {
    clearTimeout(timeout);
    $('div.collapse').addClass('in');
    $("body").append("<div id='overlay_on_side_menu_hover'></div>");
    $('#overlay_on_side_menu_hover').show().css({'filter': 'alpha(opacity=40)'});
    $('.left_side').css('z-index', 9999999);
}, function () {
    timeout = setTimeout(function () {
        $('div.collapse').removeClass('in');
        $('#overlay_on_side_menu_hover').hide();
    }, 500);

});