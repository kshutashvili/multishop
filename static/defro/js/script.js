
$(document).ready(function(){

$('#myTabs a').click(function (e) {
	  e.preventDefault()
	  $(this).tab('show')
	});

$('.owl-carousel').owlCarousel({
    items:3,
    autoWidth: true,
      margin:15,
      nav:true, 
      responsive:{
          0:{
              items:1
          },
          480:{
              items:2
          },
          620:{
              items:3
          },
          1000:{
              items:4
          },
          1200:{
              items:5
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
        $('.shadow, .modal_zakaz_zvon, .modal_mobile_sort, .buy_button_modal, .credit_button_modal, .ask_button_modal, .request_button_modal_second, .answer_button_modal, .request_button_modal_third, .request_button_modal').hide();
        if ($('.headhesive').css('display') == 'none') {
          $('.headhesive').show();
        }
        if($(window).width()<=610) {
          $('.top_menu').hide();
        }
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
        var footer_block =  $(this).siblings('.footer_info')
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
    $('.zakaz_zvon').click(function(e){
        $('.modal_zakaz_zvon').show();
        $('.shadow').show();
    });
    $('.modal_zakaz_zvon .close').click(function(){
            $('.modal_zakaz_zvon').hide();
            $('.shadow').hide();
    });
    
    headerScroll ();
    scrolbar_on();
    mobile_menu_construct ();
    searchAppend();
    $('.headhesive .more').click(function(){
        if($('.headhesive .more_contacts').hasClass('open'))
            {
                $('.headhesive .more_contacts').hide().removeClass('open');   
            }
        else
            {
                $('.headhesive .more_contacts').show().addClass('open');      
            }
    });

    // if($(window).width()<=1200) {
    //     $(".headhesive .head_menu, .header_scroll_catalog .side-menu").off("mouseenter mouseleave");
    //     $('.headhesive .head_menu').click(function(){
    //         if($('.headhesive .header_scroll_catalog').hasClass('open')) {
    //             $('.headhesive .header_scroll_catalog').hide().removeClass('open');
    //         } else {
    //             $('.headhesive .header_scroll_catalog').show().addClass('open');
    //         }
    //     });
    // } else {
    //   $('.headhesive .head_menu').unbind('click');
    //   $('.headhesive .head_menu').hover(function() {
    //     clearTimeout(timeout);
    //     $('.headhesive .header_scroll_catalog').show().addClass('open');
    //   }, function () {
    //     timeout = setTimeout(function () {
    //       $('.headhesive .header_scroll_catalog').hide().removeClass('open');
    //         }, 500);
    //   });
    // }
hover_side_menu();
$('.basket_goto.show_popup').click(function(){
  $('.headhesive').hide();
  
})
});

$(window).resize(function() {scrolbar_on(); mobile_menu_construct(); searchAppend(); resizeCatalogButton(); hover_side_menu(); hide_mobile_side_menu();});
function mobile_menu_construct ()
{
    if($(window).width()<=610) {
        $('.header_main_right .lang').appendTo( $('.main_menu'));
        $('.header_contacts div').appendTo( $('.main_menu')).addClass('header_contacts').addClass('contacts');
        $('.left_menu .dropdown a').removeAttr('data-toggle');
    } 
    else
        {
           $('.main_menu .lang').prependTo( $('.header_right'));
            $('.main_menu .header_contacts').appendTo( $('.main_contacts')).removeClass('header_contacts').removeClass('contacts');
           $('.top_menu.main_menu').show();
        }
    
}

function hover_side_menu() {
  if($(window).width()<=1200) {
        $(".headhesive .head_menu, .header_scroll_catalog .side-menu").off("mouseenter mouseleave");
        $('.headhesive .head_menu').click(function(){
            if($('.headhesive .header_scroll_catalog').hasClass('open')) {
                $('.headhesive .header_scroll_catalog').hide().removeClass('open');
            } else {
                $('.headhesive .header_scroll_catalog').show().addClass('open');
            }
        });
    } else {
      $('.headhesive .head_menu').unbind('click');
      $('.headhesive .head_menu, .header_scroll_catalog .side-menu').hover(function() {
        clearTimeout(timeout);
        $('.headhesive .header_scroll_catalog').show().addClass('open');
      }, function () {
        timeout = setTimeout(function () {
          $('.headhesive .header_scroll_catalog').hide().removeClass('open');
            }, 500);
      });
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
function headerScroll () {
    var header = new Headhesive('.header');      
    $('.headhesive .top_menu').removeClass('main_menu').addClass('scroll_menu'); 
     $('.headhesive .header_right').removeClass('header_main_right');
    $('.headhesive .header_contacts').remove();
     $('.headhesive .header_right .lang').remove();
    $('.well .left_menu').clone().appendTo('.header_scroll_catalog');
}

function resizeCatalogButton() {
  if ($(window).width()>992) {
    $('.head_menu').text('Каталог товаров');
    $('.head_menu').css('width', '264px');
  } else {
    $('.head_menu').text('Каталог');
    $('.head_menu').css('width', '150px');
  }
}

$(window).scroll(function() {
  $('.header_scroll_catalog').hide();
  $('.header_scroll_catalog').removeClass('open');
})
