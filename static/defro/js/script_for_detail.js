$(document).ready(function(){
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