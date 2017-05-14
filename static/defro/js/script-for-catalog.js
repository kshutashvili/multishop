$(document).ready(function () {

    var params = [];
    var filter_params = {};

    $('#myTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show')
    });


    $('.owl-carousel').owlCarousel({
        items: 3,
        margin: 15,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000: {
                items: 5
            }
        }
    });

    $('.bxslider_two').bxSlider({
        pagerCustom: '#bx-pager',
        minSlides: 1,
        maxSlides: 1,
        moveSlides: 1
    });
    jQuery('#scrollup img').click(function () {
        window.scroll(0, 0);
        return false;
    });

    jQuery(window).scroll(function () {
        if (jQuery(document).scrollTop() > 0) {
            jQuery('#scrollup').fadeIn('fast');
        } else {
            jQuery('#scrollup').fadeOut('fast');
        }
    });

    $(".plitka").click(function () {
        $(this).addClass("plitka_red");
        $(".spisok").removeClass("spisok_red");
        $(".catalog_items").removeClass("catalog_item_list");
    });
    $(".spisok").click(function () {
        $(this).addClass("spisok_red");
        $(".plitka").removeClass("plitka_red");
        $(".catalog_items").addClass("catalog_item_list");
    });

    var paginate_by = getParameterByName('paginate_by');

    if (paginate_by) {
        $('#paginate_by').val(paginate_by);
    }

    if (!$('.facet_checkbox.parameter_holder').length) {
        $('#applied_filters').css('display', 'none');
    }

    $('#paginate_by').change(function () {
        window.location.href = (updateQueryStringParameter(window.location.href, 'paginate_by', $(this).val()));
    });

    $('#reset_filters').click(function (e) {
        e.preventDefault();
        window.location.href = window.location.href.substring(0, window.location.href.indexOf('?'));

    });

    $('input.checkbox_filter.checkbox').change(function () {
        $('#filter_form').submit();
    });

    $('.facet').change(function (e) {
        e.preventDefault();
        e.stopPropagation();
        var full_url = $('input[name=url_for_' + $(this).attr('name')).val();
        params.push(full_url.split('/')[full_url.split('/').length - 1]);
        var val = $(this).next('.facet_label').attr('data-filter-val');
        var name = $(this).next('.facet_label').attr('data-filter-name') + '__in';
        if (name in filter_params && !$(this).prop('checked')) {
            delete filter_params[name];
        }
        else {
            filter_params[name] = val;
        }
    });

    $('.facet_label').hover(function () {
        if (!$(this).prev('input.facet').prop('checked')) {
            var val = $(this).attr('data-filter-val');
            name = $(this).attr('data-filter-name') + '__in';
            filter_params[name] = val;
            $.get('/catalugue/get_search_count/', filter_params,
                function (data) {
                    $('.filter_item_count').text(data['count']);
                });
        }
        else {
            $.get('/catalugue/get_search_count/', filter_params,
                function (data) {
                    $('.filter_item_count').text(data['count']);
                });
        }

    }, function () {
        if (!$(this).prev('input.facet').prop('checked')) {
            delete filter_params[name];
        }
    });


    $('.apply_filters').click(function () {
        var url = '';
        for (var i = 0; i < params.length; i++) {
            if (i != 0) {
                url += params[i].replace('?', '&')
            }
            else {
                url += params[i]
            }
        }
        location.href = '/catalogue/' + url;
    })
});

function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    if (uri.match(re)) {
        return uri.replace(re, '$1' + key + "=" + value + '$2');
    }
    else {
        return uri + separator + key + "=" + value;
    }
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}