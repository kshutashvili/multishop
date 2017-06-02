var timeout;

$('.dropdown.side-menu, #compare_dropdown').hover(function () {
    $(this).addClass('open');

}, function () {
    $(this).removeClass('open');

});

$('a.dropdown-toggle').click(function () {
    location.href = $(this).attr('href');
});

$('.left_side').hover(function () {
    clearTimeout(timeout);
    $('div.collapse').first().addClass('in');
}, function () {
    timeout = setTimeout(function () {
        $('div.collapse').first().removeClass('in');
    }, 500);

});