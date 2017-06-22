$(document).ready(function(){

  $('#myTabs a').click(function (e) {
	  e.preventDefault()
	  $(this).tab('show')
	});


  $('.owl-carousel').owlCarousel({
    items:3,
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

    $('.bxslider_two').bxSlider({
    pagerCustom: '#bx-pager', 
    minSlides: 1,
    maxSlides: 1,
    moveSlides: 1
  });
    jQuery('#scrollup img').click( function(){
      window.scroll(0 ,0); 
      return false;
    });

    jQuery(window).scroll(function(){
      if ( jQuery(document).scrollTop() > 0 ) {
        jQuery('#scrollup').fadeIn('fast');
      } else {
        jQuery('#scrollup').fadeOut('fast');
      }
    });

    $(".plitka").click(function(){
      $(this).addClass("plitka_red");
      $(".spisok").removeClass("spisok_red");
      $(".catalog_items").removeClass("catalog_item_list");
    });
    $(".spisok").click(function(){
      $(this).addClass("spisok_red");
      $(".plitka").removeClass("plitka_red");
      $(".catalog_items").addClass("catalog_item_list");
    });
 $('.filter_media').click(function () {
        $('.left_filter ').show();
        $('.shadow').show();
    });
    $('.shadow, .filter_submit').click(function () {
        $('.left_filter, .shadow').hide();
    });
    filterMove();
});
$(window).resize(function() {filterMove ()});
function filterMove () {
    if($(window).width()<=992)
    {
        $('.left_filter .parameters').appendTo('.mobile_filter_modal')
    }
    else
    {
        $('.left_filter .parameters').prependTo('.left_filter')
    }
}