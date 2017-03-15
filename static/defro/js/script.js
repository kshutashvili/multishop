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


});