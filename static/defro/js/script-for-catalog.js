$(document).ready(function(){

  $('#myTabs a').click(function (e) {
	  e.preventDefault()
	  $(this).tab('show')
	});

    $('#id_paginate_by').change(function () {
        $(this).closest('form').submit();
    });

    var pageNum = 2;

    $('.look_more').click(function(e) {
        var url_params = window.location.pathname;
        params = url_params.slice(1, -1);
        params = params.split('/');
        var page_param = params[params.length - 1];
        if (page_param.startsWith("p=")) {
            pageNum = parseInt(page_param.split('=').slice(-1)[0]) + 1;
            params.splice(params.length - 1);
        }
        var url = '/' + params.join("/")+ '/p=' + pageNum + '/';
        e.preventDefault();
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                $('#ul_products').append(data.content);
                $('.rating_photo').barrating({
                    theme: 'fontawesome-stars'
                });
                $(".br-widget a:first-child").css( "display", "none" );
                if (!data.has_more_pages) {
                    $('.look_more').hide();
                }
                pageNum += 1;
            },
            error: function() {
                $('.look_more').hide();
            }
        })
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
    // jQuery('#scrollup img').click( function(){
    //   window.scroll(0 ,0); 
    //   return false;
    // });

    // jQuery(window).scroll(function(){
    //   if ( jQuery(document).scrollTop() > 0 ) {
    //     jQuery('#scrollup').fadeIn('fast');
    //   } else {
    //     jQuery('#scrollup').fadeOut('fast');
    //   }
    // });

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
        $('.left_side_caption').css('z-index', '1');
    });
    $('.shadow, .filter_submit').click(function () {
        if($(window).width()<=992) {
          $('.left_filter, .shadow').hide();
        } else {
          $('.shadow').hide();
        }
        //$('.left_side_caption').css('z-index', '801');
    });

    filterMove();
    $('#filters').on('change change_price', '#filter_form input', function() {
        if ($(document).width() > 992) {
          $('#filters .filter-wrapper div').addClass('loader');
          $('#filter_form').addClass('wait');
          var desktop = true;
        }
        var input_id = $(this).attr('id');
        $.ajax({
            url: '/catalogue/update_filter/',
            type: 'GET',
            data: $('#filter_form').serialize(),
            success: function(data) {
                $('#filters').html(data['result']);
                initPrice();
                if (desktop === true) {
                    var result = '<div class="label_after"><p>'+ gettext('Товаров:') + '<span>' + data['products_count'] + '</span></p>' +
                        '<button type="submit">' + gettext('Посмотреть') + '</button></div>'
                    $('.label_after').remove();
                    $('#' + input_id).next().append(result);
                    $('.label_after').fadeIn();
                }else {
                  var result = '<div class="parameters clear_fix">' +
                    '<p class="filter_labels">' gettext('Найдено товаров:') + ' <span>' + data['products_count'] + '</span></p>' +
                    '<button class="filter_submit" type="submit">' + gettext('Посмотреть') + '</button>' +
                    '<a href="#" id="mobile_reset" class="filter_labels float_right">' gettext('Скинуть фильтр') + '</a>' +
                  '</div>';
                  $('#filters form').append(result);

                }
            },
        })
    });
    $('#filters').on('click', '#mobile_reset', function (e) {
      e.preventDefault();
      $('#filters #filter_form input:checkbox').removeAttr('checked');
    });

    $('#reset_filters').click(function (e) {
      e.preventDefault();
      var url_params = window.location.pathname;
      params = url_params.slice(1, -1);
      params = params.split('/');
      var filter_param = params[params.length - 1];
      url_params = url_params.replace(filter_param, '');
      url_params = url_params.replace('//', '/');
      window.location.pathname = url_params;
    });

    $('.filter-facet-clear').click(function (e) {
        e.preventDefault();
        $('#' + $(this).data('checkbox-id')).removeAttr('checked');
        $('#filter_form').submit();
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