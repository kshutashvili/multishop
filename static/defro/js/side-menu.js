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
}, function () {
    timeout = setTimeout(function () {
        $('div.collapse').removeClass('in');
    }, 500);

});