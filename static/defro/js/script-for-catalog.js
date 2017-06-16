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
        $('.left_side_caption').css('z-index', '799');
    });
    $('.shadow, .filter_submit').click(function () {
        if($(window).width()<=992) {
          $('.left_filter, .shadow').hide();
        } else {
          $('.shadow').hide();
        }
        $('.left_side_caption').css('z-index', '801');
    });
    filterMove();
    $('#filters').on('change change_price', '#filter_form input', function() {
        $('#filters .filter-wrapper div').addClass('loader');
        $('#filter_form').addClass('wait');
        var input_id = $(this).attr('id');
        $.ajax({
            url: '/catalogue/update_filter/',
            type: 'GET',
            data: $('#filter_form').serialize(),
            success: function(data) {
                $('#filters').html(data['result']);
                initPrice();
                var result = '<div class="label_after"><p>Товаров: <span>' + data['products_count'] + '</span></p>' +
                    '<button type="submit">Посмотреть</button></div>'
                $('.label_after').remove();
                $('#' + input_id).next().append(result);
                $('.label_after').fadeIn();
            },
        })
    })

    $('.filter-facet-clear').click(function (e) {
        e.preventDefault()
        var name = $(this).closest('p').find('input[name="field_name"]').val();
        var value = $(this).closest('p').find('input[name="field_value"]').val();
        var get_query = decodeURIComponent(window.location.search.substr(1))
        var get_query_array = get_query.split('&');
        for (var i=0; i < get_query_array.length; i++) {
            var key_value = get_query_array[i].split('=');

            if (key_value[0] == name && key_value[1] == value) {
                get_query = get_query.replace(get_query_array[i], '');
                get_query = get_query.replace('&&', '&');
                window.location.search = get_query;
            }
        }
    });
});

$(window).resize(function() {filterMove ()});
function filterMove () {
    if($(window).width()<=992)
    {
        $('.left_filter .parameters').appendTo('.mobile_filter_modal')
    }
    else
    {
        $('.left_filter').show();
        $('.left_filter .parameters').prependTo('.left_filter')
    }
}