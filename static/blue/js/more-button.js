 $(document).ready(function ()
	  {  var h = 300, t = $('#tovar_desc'), max = t[0].scrollHeight, min = 0, scoreA = 0;
	   $('.read-next').on('click', function (event)
	  {
	   var H = t.height();
	   if(scoreA == 0){
	   	$('.read-next').addClass("read-next-arrow");
	   	scoreA = 1;
	   }else{
	   	$('.read-next').removeClass("read-next-arrow");
	   	scoreA = 0;
	   }

	   if(H == max){H = min}
	   else if (H  + h > max){H = max}
	   else {H += h};
	   t.height(H);
	   $(this).text(H == max ? 'Свернуть' : 'Читать далее')
	   return false
	  })
	  });


	 $('.read-next-fullcomment').on('click', function(){
        is_parent = $(this).parent(); 
        blok = is_parent.find('.comment_range');
        if(blok.css('max-height') != 'none'){
           blok.css('max-height','');
           $(this).text('Свернуть');
           $(this).addClass("read-next-arrow");
        } else {
           blok.css('max-height','522px');    
           $(this).text('Читать все отзывы');
           $(this).removeClass("read-next-arrow");
        }
         
        return false;
    });


 		$('.read-next-comment').on('click', function(){
        is_parent = $(this).parent(); 
        blok = is_parent.find('.user_comment');
        if(blok.css('max-height') != 'none'){
           blok.css('max-height','');
           $(this).text('Свернуть');
           $(this).addClass("read-next-arrow");
        } else {
           blok.css('max-height','53px');    
           $(this).text('Читать далее');
           $(this).removeClass("read-next-arrow");
        }
         
        return false;
    });

     
    $('.read-next-com').on('click', function(){
        is_parent = $(this).parent(); 
        blok = is_parent.find('.user_comment');
        if(blok.css('max-height') != 'none'){
           blok.css('max-height','');
           $(this).text('Свернуть');
           $(this).addClass("read-next-arrow");
        } else {
           blok.css('max-height','50px');    
           $(this).text('Читать далее');
           $(this).removeClass("read-next-arrow");
        }
         
        return false;
    });
