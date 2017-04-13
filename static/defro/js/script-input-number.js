$(document).ready(function () {

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

        return false;
    });
});
