$(document).ready(function() {
    $('.minus').click(function () {
        var $input = $(this).parent().parent().find('.input_number');
        var $input2 = $(this).parent().parent().find('.how.much input');

        var count = parseInt($input.val());
        var count2 = parseInt($input2.val());

        
         if (count === 1){
            count2 = count2;
        }else{
            count2 = count2/2;            
        }
        count = count - 1;
        count = count < 1 ? 1 : count;
               
        $input.val(count);
        $input2.val(count2);


        $input.change();
        $input2.change();

        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().parent().find('.input_number');
        var $input2 = $(this).parent().parent().find('.how.much input');

        $input.val(parseInt($input.val()) + 1);
        $input2.val(parseInt($input2.val())*2);

        $input.change();
        $input2.change();

        return false;
    });
});
