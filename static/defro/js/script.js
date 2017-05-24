var header = new Headhesive('.header');
$(document).ready(function(){

  $('#myTabs a').click(function (e) {
	  e.preventDefault()
	  $(this).tab('show')
	});

  $('.owl-carousel').owlCarousel({
    items:3,
      margin:25,
      nav:true, 
      responsive:{
          0:{
              items:1
          },
          600:{
              items:3
          },
          1000:{
              items:6
          }
      }
  });

    $('.bxslider').bxSlider({
      minSlides: 1,
      maxSlides: 1,
      auto: true,
      moveSlides: 1,
      pause: 3000
    });

    $('.mobile_menu').click(function () {
        $('.top_menu').show();
        $('.shadow').show();
    });
    $('.shadow').click(function () {
        $('.top_menu, .shadow').hide();
    });
    $('.more_block').click(function () {
        var more_block =  $(this).siblings('.more_info')
            if(more_block.hasClass('info_show'))
            {
                more_block.hide().removeClass('info_show');
                $(this).find('p').text('Подробнее');
            }
            else
            {
                more_block.show().addClass('info_show');
                $(this).find('p').text('Свернуть');
            }
    });
    $('.list_more').click(function (e) {
        var more_block =  $(this).parent('.list_caption').siblings('.first_ul ')
        if(more_block.hasClass('info_show'))
        {
            more_block.hide().removeClass('info_show');
            $(this).find('p').text('Подробнее');
        }
        else
        {
            more_block.show().addClass('info_show');
            $(this).find('p').text('Свернуть');
        }
    });
    $('.list_more_second').click(function (e) {
        var more_block =  $(this).parent('.list_caption').siblings('.second_ul ')
        if(more_block.hasClass('info_show'))
        {
            more_block.hide().removeClass('info_show');
            $(this).find('p').text('Подробнее');
        }
        else
        {
            more_block.show().addClass('info_show');
            $(this).find('p').text('Свернуть');
        }
    });
    $('.footer_close').click(function () {
        var footer_block =  $(this).sibling('.footer_info')
            if(footer_block.hasClass('footer_show'))
            {
                footer_block.hide().removeClass('footer_show');
                $(this).removeClass('footer_open')
            }
            else
            {
                footer_block.show().addClass('footer_show');
                $(this).addClass('footer_open')
            }
    });
    $('.sort_vid .sort').click(function(){
         if($(window).width()<=672)
         {
            $('.modal_mobile_sort').show();
            $('.shadow').show();
         }
    })
    $('.modal_mobile_sort .close').click(function(){
            $('.modal_mobile_sort').hide();
            $('.shadow').hide();
    });
    scrolbar_on();
    colapsehide ();
    mobile_menu_construct ();
    searchAppend();
});
$(window).resize(function() {colapsehide (); scrolbar_on(); mobile_menu_construct (); searchAppend()});
function mobile_menu_construct ()
{
    if($(window).width()<=610) {
        $('.header_right .lang').appendTo( $('.top_menu'));
        $('.header_contacts').appendTo( $('.top_menu'));
    } 
    
}

function colapsehide () {
    if($(window).width()<=460)
    {
        $('#collapseExample').removeClass('in');
        $('.left_side_caption').click(function () {
            $('.shadow').toggle();
        });
        $('.shadow').click(function () {
            $('#collapseExample').removeClass('in');
        })
    }
    else
    {
        $('#collapseExample').addClass('in');
    }
}
function scrolbar_on() {
    if($(window).width()<=672) {
        $('.scrollbar-inner').scrollbar();
    }
}
function searchAppend() {
            if($(window).width()<=992) {
                $('.left_filter .search_parameters .caption').prependTo( $('.sort_vid'));
            }
}