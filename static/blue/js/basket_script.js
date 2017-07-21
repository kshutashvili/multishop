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
    $('.minus, .plus').off();
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


function modal_item_factory(img, upc, name, price, id, quantity) {
    var $container = $('<div class="modal_basket_elem" id="' + id + '"></div>');
    var $img = $('<img src="' + img + '" />');
    var $modal_article = $('<p class="modal_article">Артикул: <span>' + upc + '</span></p>');
    var $name = $('<p class="modal_item_name">' + name + '</p>');
    var $many_block = $('<div class="how many many_block"></div>');
    var $plusminus = $('<div class="plusminus"></div>');
    var $input1 = $('<input type="text" disabled id="input1" value="' + quantity + '" class="input_number" data-product-id="' + id + '">');
    var $input2 = $('<input type="text" class="price_for_one" style="display: none" value="' + price + '">');
    var $input3 = $('<input type="text" class="item_quantity" style="display: none" value="1">');
    var $plusminus_cont = $('<div class="plusminus_cont"><span class="plus">+</span><span class="minus">-</span></div>');
    var $how_much = $('<div class="how much"><input type="text" id="input2" name="price" value="' + price * quantity + '" disabled></div>');
    var $delete = $('<a href="#!" data-url="/basket/delete_item_from_basket/' + id + '/" class="modal_item_delete"></a>');


    $plusminus.append($input1, $input2, $input3, $plusminus_cont, $how_much);
    $many_block.append($plusminus);
    $container.append($img, $modal_article, $name, $many_block, $delete);

    return $container;
}

function basket_dropdown_item_factory(img, name, quantity, price) {
    var $container = $('<div class="basket_elem"></div>');
    var $img = $('<img src="' + img + '" />');
    var $name = $('<p class="basket_item_name">' + name + '</p>');
    var $quantity = $('<p class="basket_item_number">' + quantity + ' шт</p>');
    var $price = $('<p class="basket_item_price">' + price * quantity + 'грн</p>');

    $container.append($img, $name, $quantity, $price);
    return $container;

}

function update_modal_lines_info() {
    var $basket_items = $('.modal_basket_elem');
    var $modal_line_count = $('#modal_line_count');
    var $modal_lines_price = $('.how.much input');
    var $total_sum = $('#total_sum');
    var $total_sum_bottom = $('#total_sum_bottom');
    var $total_in_dropdown = $('#total_in_dropdown');
    var $dropdown_line_count = $('#dropdown_line_count');
    var total = 0;
    $modal_lines_price.map(function (idx, elem) {
        total += parseInt($(elem).val());
    });
    $modal_line_count.text($basket_items.length + ' товар');
    $dropdown_line_count.text($basket_items.length + ' товаров');
    $total_sum.text(parseInt(total));
    $total_sum_bottom.text(parseInt(total));
    $total_in_dropdown.text(parseInt(total) + ' грн.');
    $('#dropdownMenu2').attr('data-content', $basket_items.length);  // count on basket icon in header

}


$(document).ready(function () {
    var $comment_form = $('#review_form');
    var review_url = $comment_form.prop('action');

    var $basket_items = $('#basket_items');
    var $basket_dropdown = $('#basket_dropdown');

    var in_basket = [];

    function update_basket_info() {
        $.get($basket_dropdown.attr('data-basket-url'), function (data) {
            try {
                data['basket_products'].forEach(function (element) {
                    var $new_item = modal_item_factory(element['img'], element['upc'], element['title'], element['price'], element['id'], element['quantity']);
                    var $new_dropdown_element = basket_dropdown_item_factory(element['img'], element['title'], element['quantity'], element['price']);

                    $basket_items.append($new_item);
                    $new_dropdown_element.appendTo(basket_dropdown);
                    in_basket.push(element['upc']);
                });
            }
            catch (e) {
            }

            change_numbers();
            modal_item_delete();
            update_modal_lines_info();

        });
    }

    update_basket_info();


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
        $.post(url_buy, $form_buy.serialize(), function (data) {
            if (!data['errors']) {
                if (in_basket.indexOf(data['upc']) == -1) {
                    var $new_item = modal_item_factory(data['img'], data['upc'], data['title'], data['price'], data['id'], 1);
                    var $new_dropdown_element = basket_dropdown_item_factory(data['img'], data['title'], 1, data['price']);

                    $basket_items.append($new_item);
                    $basket_dropdown.append($new_dropdown_element);
                    in_basket.push(data['upc']);
                    change_numbers();
                    modal_item_delete();


                    update_modal_lines_info();
                }
                else {
                    $('div#' + data['id'] + '.modal_basket_elem').find('.plus').trigger('click');
                }

                $('div.' + $(this).attr("rel")).fadeIn(500);
                //$("body").append("<div id='overlay'></div>");
                //$('#overlay').show().css({'filter': 'alpha(opacity=80)'});
                $('.shadow').show();
            }
            else {
                var $errors = $('#basket_error');
                $errors.text(data['errors']);
                $errors.addClass('show');
                setTimeout(function () {
                    $errors.removeClass("show");
                }, 3000);
            }
        });
    });


    $('#submit_comment').click(function (e) {
        e.preventDefault();
        $.post(review_url, $comment_form.serialize(), function () {
            $comment_form.find("input[type=text], textarea").val("");
            $('div.' + $('#submit_comment').attr("rel")).fadeIn(500);
            //$("body").append("<div id='overlay'></div>");
            //$('#overlay').show().css({'filter': 'alpha(opacity=80)'});
            $('.shadow').show();
            return false;
        }).fail(function (xhr) {
            if (parseInt(xhr.status) == 409) {
                var $errors = $('#basket_error');
                $errors.text('Вы можете оставить только один отзыв!');
                $errors.addClass('show');
                setTimeout(function () {
                    $errors.removeClass("show");
                }, 3000);
            }
        });
    });
    $('#submit_comment1').click(function (e) {
        e.preventDefault();
        $.post(review_url, $comment_form.serialize(), function () {
            $comment_form.find("input[type=text], textarea").val("");
            $('div.' + $('#submit_comment1').attr("rel")).fadeIn(500);
            $('.shadow').show();
            return false;
        }).fail(function (xhr) {
            if (parseInt(xhr.status) == 409) {
                var $errors = $('#basket_error');
                $errors.text('Вы можете оставить только один отзыв!');
                $errors.addClass('show');
                setTimeout(function () {
                    $errors.removeClass("show");
                }, 3000);
            }
        });
    });
    function modal_item_delete() {
        $('.modal_item_delete').click(function (e) {
            e.preventDefault();
            $.post($(this).attr('data-url'), function () {
                location.reload();
            });
        });
    }


    $('#one_click_btn').click(function (e) {
        e.preventDefault();
        var outer_this = this;
        $.post($(this).attr('data-oneclick-url'), $('#buy_one_click').serialize(), function () {
            $('div.' + $(outer_this).attr("rel")).fadeIn(500);
            //$("body").append("<div id='overlay'></div>");
            //$('#overlay').show().css({'filter': 'alpha(opacity=80)'});
            $('.shadow').show();
        }).fail(function () {
            // Get the snackbar DIV
            var x = document.getElementById("snackbar");

            // Add the "show" class to DIV
            x.className += " show";

            // After 3 seconds, remove the show class from DIV
            setTimeout(function () {
                x.className = x.className.replace("show", "");
            }, 3000);
        });
    });

    $('#one_click_btn_modal').click(function (e) {
        e.preventDefault();
        var outer_this = this;
        $.post($(this).attr('data-oneclick-url'), $('#buy_one_click_modal').serialize(), function (data) {
            $('.close').trigger('click');
            $('div.' + $(outer_this).attr("data-rel")).fadeIn(500);
            //$("body").append("<div id='overlay'></div>");
            //$('#overlay').show().css({'filter': 'alpha(opacity=80)'});
            $('.shadow').show();
            setTimeout(function () {
                location.href = data;
            }, 3000);
        }).fail(function () {
            // Get the snackbar DIV
            var x = document.getElementById("snackbar");

            // Add the "show" class to DIV
            x.className += " show";

            // After 3 seconds, remove the show class from DIV
            setTimeout(function () {
                x.className = x.className.replace("show", "");
            }, 3000);
            return false;
        });
    });

    $('a.elipse_button#comp, a.compare_button').click(function (e) {
        e.preventDefault();
        if ($(this).attr('data-compare-url')) {
            $.post($(this).attr('data-compare-url'), {'id': $(this).attr('data-product-id')}, function () {
                var x = document.getElementById("compare_success");

                // Add the "show" class to DIV
                x.className += " show";

                // After 3 seconds, remove the show class from DIV
                setTimeout(function () {
                    x.className = x.className.replace("show", "");
                    location.reload();
                }, 1000);
            });
        }
    });

    $('.close_compare').click(function (e) {
        e.preventDefault();
        $.post($(this).attr('data-remove-url'), {'id': $(this).attr('data-product-id')}, function () {
            location.reload();
        });
    });

    $('.sravn_delete, .compare_table_clean_button').click(function (e) {
        e.preventDefault();
        $.post($(this).attr('data-remove-url'), {'pk': $(this).attr('data-category-pk')}, function () {
            location.reload();
        });
    });

    $('#make_order, #continue_shopping, #checkout_dropdown').click(function (e) {
        e.preventDefault();
        var outer_this = this;
        var quantity = {};
        $.each($('.input_number'), function (index, value) {
            quantity[$(value).attr('data-product-id')] = $(value).val();
        });
        if (in_basket.length) {
            $.post($(this).attr('data-update-url'), quantity, function (data) {
                if (!data['errors']) {
                    if ($(outer_this).attr('id') == 'continue_shopping') {
                        $basket_dropdown.html('');
                        $basket_items.html('');
                        update_basket_info();
                        if (~location.href.indexOf('basket')) {
                            location.href = $(outer_this).attr('data-catalogue-url');
                        }
                    }
                    else {
                        location.href = $(outer_this).attr('data-checkout-url');
                    }
                }
                else {
                    var $errors = $('#basket_error');
                    $errors.text(data['errors']);
                    $errors.addClass('show');
                    setTimeout(function () {
                        $errors.removeClass("show");
                    }, 3000);
                }
            });
        }


    });

    $("#print").click(function (e) {
        e.preventDefault();
        window.print();
    });

    $('#submit_call_request').click(function (e) {
        e.preventDefault();
        var outer_this = this;
        $.post($('#call_request_form').attr('action'), $('#call_request_form').serialize(), function () {
            $('.close').trigger('click');
            $('div.' + $(outer_this).attr("data-rel")).fadeIn(500);
            //$("body").append("<div id='overlay'></div>");
            //$('#overlay').show().css({'filter': 'alpha(opacity=80)'});
            $('.shadow').show();
            return false;
        });
    });

});
