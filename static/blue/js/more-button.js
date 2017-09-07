$(document).ready(function () {
    var h = 300, t = $('#tovar_desc'), max = t[0].scrollHeight, min = 0,
        scoreA = 0;
    $('.read-next').on('click', function (event) {
        var H = t.height();

        var tables = $('#tovar_desc table');
        var tables_height = 0;
        for (var i = 0; i < tables.length; i++) {
            tables_height += tables[i].scrollHeight;
        }

        if (scoreA == 0) {
            $('.read-next').addClass("read-next-arrow");
            $('#short_desc').hide();
            t.addClass('fulltext');
            $(this).text(gettext('Свернуть'));
            scoreA = 1;
        } else {
            $('.read-next').removeClass("read-next-arrow");
            $('#short_desc').show();
            t.removeClass('fulltext');
            $(this).text(gettext('Подробнее'));
            scoreA = 0;
        }
        return false
    })
});


	 $('.read-next-fullcomment').on('click', function(){
        is_parent = $(this).parent(); 
        blok = is_parent.find('.comment_range');
        if(blok.css('max-height') != 'none'){
           blok.css('max-height','');
           $(this).text(gettext('Свернуть'));
           $(this).addClass("read-next-arrow");
        } else {
           blok.css('max-height','522px');    
           $(this).text(gettext('Читать все отзывы'));
           $(this).removeClass("read-next-arrow");
        }
         
        return false;
    });


 		$('.read-next-comment').on('click', function(){
        is_parent = $(this).parent(); 
        blok = is_parent.find('.user_comment');
        if(blok.css('max-height') != 'none'){
           blok.css('max-height','');
           $(this).text(gettext('Свернуть'));
           $(this).addClass("read-next-arrow");
        } else {
           blok.css('max-height','53px');    
           $(this).text(gettext('Читать далее'));
           $(this).removeClass("read-next-arrow");
        }
         
        return false;
    });

     
    $('.read-next-com').on('click', function(){
        is_parent = $(this).parent(); 
        blok = is_parent.find('.user_comment');
        if(blok.css('max-height') != 'none'){
           blok.css('max-height','');
           $(this).text(gettext('Свернуть'));
           $(this).addClass("read-next-arrow");
        } else {
           blok.css('max-height','50px');    
           $(this).text(gettext('Читать далее'));
           $(this).removeClass("read-next-arrow");
        }
         
        return false;
    });
