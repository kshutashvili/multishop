/**
 * Created by dmitry on 4/13/17.
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function () {
    var $comment_form = $('#review_form');
    var review_url = $comment_form.prop('action');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $('.buy_button, #submit_btn').click(function (e) {
        e.preventDefault();
        var $form_buy = $('form#add_to_basket_form_' + $(this).attr('data-product-id'));
        var url_buy = $form_buy.prop('action');
        $('#modal_product_' + $(this).attr('data-product-id')).show();
        $.post(url_buy, $form_buy.serialize(), function () {
            $('div.' + $(this).attr("rel")).fadeIn(500);
            $("body").append("<div id='overlay'></div>");
            $('#overlay').show().css({'filter': 'alpha(opacity=80)'});
        });
    });

    $('#submit_comment').click(function (e) {
        e.preventDefault();
        $.post(review_url, $comment_form.serialize(), function () {
            $comment_form.find("input[type=text], textarea").val("");
            $('div.' + $('#submit_comment').attr("rel")).fadeIn(500);
            $("body").append("<div id='overlay'></div>");
            $('#overlay').show().css({'filter': 'alpha(opacity=80)'});
            return false;
        });
    });

    $('.modal_item_delete').click(function (e) {
        e.preventDefault();
        $.post($(this).attr('data-url'), function () {
            location.reload();
        });
    });
});
