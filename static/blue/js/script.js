
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
        $('.top_menu, .shadow, .modal_zakaz_zvon, .modal_mobile_sort').hide();
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
    colapsehide ();
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
    $('.headhesive .mobile_menu').click(function(){
        if($('.headhesive .header_scroll_catalog').hasClass('open'))
            {
                $('.headhesive .header_scroll_catalog').hide().removeClass('open');   
            }
        else
            {
                $('.headhesive .header_scroll_catalog').show().addClass('open');      
            }
    });
    
   
});
$(window).resize(function() {colapsehide (); scrolbar_on(); mobile_menu_construct (); searchAppend();});
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
           
        }
    
}

function colapsehide () {
    if($(window).width()<=460)
    {
        $('#collapseExample').removeClass('in');
        $('.left_side_caption').click(function () {
            if($('#collapseExample').hasClass('in'))
            {
                $('.shadow').hide();
            }
            else
            {
                $('.shadow').show();
            }
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
function headerScroll ()
{
    var header = new Headhesive('.header');      
    $('.headhesive .top_menu').removeClass('main_menu').addClass('scroll_menu'); 
     $('.headhesive .header_right').removeClass('header_main_right');
    $('.headhesive .header_contacts').remove();
     $('.headhesive .header_right .lang').remove();
    $('.well .left_menu').clone().appendTo('.header_scroll_catalog');
    
}