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


    function change_numbers() {
        $('.minus').click(function () {
        var $input = $(this).parent().parent().find('.input_number');  // quantity
        var $input2 = $(this).parent().parent().find('.how.much input'); // price

        var price_for_item = parseInt($(this).parent().parent().find('.price_for_one').val());

        var quantity = parseInt($input.val());
        var price;

        if (quantity > 1) {
            quantity--;
            price = price_for_item * quantity;
            $input.val(quantity);
            $input2.val(price);
            $input.change();
            $input2.change();
        }
        update_modal_lines_info();
        return false;
    });

    $('.plus').click(function () {
        var $input = $(this).parent().parent().find('.input_number');
        var $input2 = $(this).parent().parent().find('.how.much input');

        var price_for_item = parseInt($(this).parent().parent().find('.price_for_one').val());

        var quantity = parseInt($input.val());
        var price;

        quantity++;
        price = price_for_item * quantity;
        $input.val(quantity);
        $input2.val(price);
        $input.change();
        $input2.change();

        update_modal_lines_info();

        return false;
    });
    }

    change_numbers();



function modal_item_factory(img, upc, name, price, id) {
    var $container = $('<div class="modal_basket_elem"></div>');
    var $img = img;
    var $modal_article = $('<p class="modal_article">Артикул: <span>' + upc + '</span></p>');
    var $name = $('<p class="modal_item_name">' + name + '</p>');
    var $many_block = $('<div class="how many many_block"></div>');
    var $plusminus = $('<div class="plusminus"></div>');
    var $input1 = $('<input type="text" disabled id="input1" value="1" class="input_number">');
    var $input2 = $('<input type="text" class="price_for_one" style="display: none" value="' + price + '">');
    var $input3 = $('<input type="text" class="item_quantity" style="display: none" value="1">');
    var $plusminus_cont = $('<div class="plusminus_cont"><span class="plus">+</span><span class="minus">-</span></div>');
    var $how_much = $('<div class="how much"><input type="text" id="input2" name="price"value="' + price + '" disabled></div>');
    var $delete = $('<a href="" data-url="delete_item_from_basket/' + id + '" class="modal_item_delete"></a>');


    $plusminus.append($input1, $input2, $input3, $plusminus_cont, $how_much);
    $many_block.append($plusminus);
    $container.append($img, $modal_article, $name, $many_block, $delete);

    return $container;
}

function update_modal_lines_info() {
    var $basket_items = $('.modal_basket_elem');
    var $modal_line_count = $('#modal_line_count');
    var $modal_lines_price = $('.how.much input');
    var $total_sum = $('#total_sum');
    var $total_sum_bottom = $('#total_sum_bottom');
    var total = 0;
    $modal_lines_price.map(function (idx, elem) {
        total += parseInt($(elem).val());
    });
    $modal_line_count.text($basket_items.length + ' товар');
    $total_sum.text(parseInt(total));
    $total_sum_bottom.text(parseInt(total));


}


$(document).ready(function () {
    var $comment_form = $('#review_form');
    var review_url = $comment_form.prop('action');

    var in_basket = [];
    $('span[name="product_upc"]').map(function (idx, elem) {
        in_basket.push($(elem).text());
    });

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }

    });

    $('.buy_button, #submit_btn').click(function (e) {
        e.preventDefault();
        var $outer_this = $(this);
        var $form_buy = $('form#add_to_basket_form_' + $(this).attr('data-product-id'));
        var url_buy = $form_buy.prop('action');
        $('#modal_product_' + $(this).attr('data-product-id')).show();
        $.post(url_buy, $form_buy.serialize(), function () {

            upc = $outer_this.parent().find('input[name="upc"]').val();

            if (parseInt(in_basket.indexOf(upc)) == -1 && upc) {
                $image = $outer_this.parent().find('img').clone();

                name = $outer_this.parent().find('p.catalog_item_block_caption').text();
                price = $outer_this.parent().find('p.catalog_item_price').text();
                id = $outer_this.parent().find('input[name="id"]').val();
                $new_item = modal_item_factory($image, upc, name, price, id);

                $('#basket_items').append($new_item);
                in_basket.push(upc);
                change_numbers();
            }

            update_modal_lines_info();


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
