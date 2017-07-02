var timeout;

$('.dropdown.side-menu').hover(function () {
    $(this).addClass('open');

}, function () {
    $(this).removeClass('open');

});

$('#compare_dropdown').hover(function () {
    $(this).addClass('open');

}, function () {
    $(this).removeClass('open');

});

function hide_mobile_side_menu () {
    if($(window).width()<=610) {
        $('.dropdown.side-menu .dropdown-menu').addClass('mobile-hide');
        $('.headhesive').addClass('mobile-hide');
        $('.left_side_caption').css('z-index', '1');
    }
    else {
        $('.dropdown.side-menu .dropdown-menu').removeClass('mobile-hide');
        $('.headhesive').removeClass('mobile-hide');
        $('.left_side_caption').css('z-index', '801');
    }
}


$('a.dropdown-toggle').click(function () {
    location.href = $(this).attr('href');
});

function side_hover () {
    $( ".left_side_caption, #collapseExample .well" ).off( "mouseenter mouseleave" );
    if($(window).width()>595){
        $('.left_side_caption, #collapseExample .well').hover(function () {
            clearTimeout(timeout);
            $('.left_side_caption, .left_menu').addClass('shadow_hover');
            $('div.collapse').first().addClass('in');
            $('.shadow').show();
        }, function () {
            timeout = setTimeout(function () {
                $('div.collapse').first().removeClass('in');
                $('.left_side_caption, .left_menu').removeClass('shadow_hover');
                $('.shadow').hide();
            }, 500);
        });
    } else {
        $( ".left_side_caption, #collapseExample .well" ).off( "mouseenter mouseleave" );
        $('.shadow').click(function () {
            $('#collapseExample').removeClass('in');
        })
        $('.left_side_caption').click(function () {
            if($('#collapseExample').hasClass('in')) {
                $('.left_side_caption, .left_menu').removeClass('shadow_hover');
                $('.shadow').hide();
            }
            else {
                $('.left_side_caption, .left_menu').addClass('shadow_hover');
                $('.shadow').show();
            }
        });
    }
}

function side_hover_landing () {
    $(".left_side_caption, .well").off("mouseenter mouseleave");
    if($(window).width()<=460) {
        $(".left_side_caption, .well").off("mouseenter mouseleave");
        $('#collapseExample').removeClass('in');
        $('.shadow').click(function () {
            $('#collapseExample').removeClass('in');
            $('.left_side_caption, .left_menu').removeClass('shadow_hover');
            $('.shadow').hide();
        })
        $('.left_side_caption').click(function () {
            if($('#collapseExample').hasClass('in')) {
                $('.left_side_caption, .left_menu').removeClass('shadow_hover');
                $('.shadow').hide();
                $('div.collapse').first().removeClass('in');
            }
            else {
                $('.left_side_caption, .left_menu').addClass('shadow_hover');
                $('.shadow').show();
                $('#collapseExample').addClass('in');
            }
        });
    } else {
        $('#collapseExample').addClass('in');
        $('.left_side_caption').unbind('click');
        $('.shadow').unbind('click');
        $('.left_side_caption, .well').hover(function () {
            clearTimeout(timeout);
            $('.left_side_caption, .left_menu').addClass('shadow_hover');
            $('.shadow').show();
            $('div.collapse').first().addClass('in');
        }, function () {
            timeout = setTimeout(function () {
                $('.left_side_caption, .left_menu').removeClass('shadow_hover');
                $('.shadow').hide();
            }, 500);
        });
    }
}
