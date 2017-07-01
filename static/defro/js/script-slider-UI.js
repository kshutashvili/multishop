function initPrice() {
  min = 0;
  max = jQuery("#slider_price").data('max-price');
  price_range_min = jQuery("#slider_price").data('price-range-min');
  price_range_max = jQuery("#slider_price").data('price-range-max');

  if ('' !== price_range_max && '' !== price_range_min) {
    values = [price_range_min, price_range_max];
  }
  else {
    values = [min, max];
  }
  jQuery("#slider_price").slider({
    min: min,
    max: max,
    values: values,
    range: true,
        stop: function(event, ui) {
            jQuery("input#minCost").val(jQuery("#slider_price").slider("values",0));
            jQuery("input#maxCost").val(jQuery("#slider_price").slider("values",1));
            jQuery("input#maxCost").trigger('change_price');
        },
        slide: function(event, ui){
            jQuery("input#minCost").val(jQuery("#slider_price").slider("values",0));
            jQuery("input#maxCost").val(jQuery("#slider_price").slider("values",1));
        },
  });

  jQuery("input#minCost").change(function(){
    var value1=jQuery("input#minCost").val();
    var value2=jQuery("input#maxCost").val();
    if (value2 == '') {
      max = jQuery("#slider_price").slider("option", "max");
      value2 = max;
      jQuery("input#maxCost").val(max);
    }
    if(parseInt(value1) > parseInt(value2)){
      value1 = value2;
      jQuery("input#minCost").val(value1);
    }
    jQuery("#slider_price").slider("values",0,value1);  
  });

    
  jQuery("input#maxCost").change(function(){
    var value1=jQuery("input#minCost").val();
    var value2=jQuery("input#maxCost").val();
    if (value1 == '') {
      jQuery("input#minCost").val(0);
    }
    
    if(parseInt(value1) > parseInt(value2)){
      value2 = value1;
      jQuery("input#maxCost").val(value2);
    }
    jQuery("#slider_price").slider("values",1,value2);
  });

  jQuery('input#maxCost').keypress(function(event){
      var key, keyChar;
      if(!event) var event = window.event;
      
      if (event.keyCode) key = event.keyCode;
      else if(event.which) key = event.which;
    
      if(key==null || key==0 || key==8 || key==13 || key==9 || key==46 || key==37 || key==39 ) return true;
      keyChar=String.fromCharCode(key);
      
      if(!/\d/.test(keyChar)) return false;
    
    });
  jQuery('input#minCost').keypress(function(event){
      var key, keyChar;
      if(!event) var event = window.event;
      
      if (event.keyCode) key = event.keyCode;
      else if(event.which) key = event.which;
    
      if(key==null || key==0 || key==8 || key==13 || key==9 || key==46 || key==37 || key==39 ) return true;
      keyChar=String.fromCharCode(key);
      
      if(!/\d/.test(keyChar)) return false;
    
    });
}

$(document).ready(function(){
  jQuery("input#minCost").val('');
  jQuery("input#maxCost").val('');
  initPrice();

});