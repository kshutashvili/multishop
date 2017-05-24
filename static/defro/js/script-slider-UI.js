$(document).ready(function(){

jQuery("#slider_price").slider({
  min: 0,
  max: 30000,
  values: [5000,20000],
  range: true,
      stop: function(event, ui) {
          jQuery("input#minCost").val(jQuery("#slider_price").slider("values",0));
          jQuery("input#maxCost").val(jQuery("#slider_price").slider("values",1));
      },
      slide: function(event, ui){
          jQuery("input#minCost").val(jQuery("#slider_price").slider("values",0));
          jQuery("input#maxCost").val(jQuery("#slider_price").slider("values",1));
      }
});

jQuery("input#minCost").change(function(){
  var value1=jQuery("input#minCost").val();
  var value2=jQuery("input#maxCost").val();

    if(parseInt(value1) > parseInt(value2)){
    value1 = value2;
    jQuery("input#minCost").val(value1);
  }
  jQuery("#slider_price").slider("values",0,value1);  
});

  
jQuery("input#maxCost").change(function(){
  var value1=jQuery("input#minCost").val();
  var value2=jQuery("input#maxCost").val();
  
  if (value2 > 1000) { value2 = 1000; jQuery("input#maxCost").val(1000)}

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



  $( function() {
    var select = $( "#minbeds" );
    var slider = $( "#slider_month" ).slider({
      min: 1,
      max: 6,
      range: "min",
      value: select[ 0 ].selectedIndex + 1,
      slide: function( event, ui ) {
        select[ 0 ].selectedIndex = ui.value - 1;
      }
    });
    $( "#minbeds" ).on( "change", function() {
      slider.slider( "value", this.selectedIndex + 1 );
    });
  } );

  $( function() {
    var select = $( "#minbeds2" );
    var slider = $( "#slider_month2" ).slider({
      min: 1,
      max: 6,
      range: "min",
      value: select[ 0 ].selectedIndex + 1,
      slide: function( event, ui ) {
        select[ 0 ].selectedIndex = ui.value - 1;
      }
    });
    $( "#minbeds2" ).on( "change", function() {
      slider.slider( "value", this.selectedIndex + 1 );
    });
  } );

  $( function() {
    var select = $( "#minbeds3" );
    var slider = $( "#slider_month3" ).slider({
      min: 1,
      max: 6,
      range: "min",
      value: select[ 0 ].selectedIndex + 1,
      slide: function( event, ui ) {
        select[ 0 ].selectedIndex = ui.value - 1;
      }
    });
    $( "#minbeds3" ).on( "change", function() {
      slider.slider( "value", this.selectedIndex + 1 );
    });
  } );



});