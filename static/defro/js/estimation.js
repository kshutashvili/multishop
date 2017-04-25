const estimate_power = () => {
	const square = $('#t_square').val()
	if (square < 0) { 
		$('#t_power').html('0')
		$('#t_season').html('0')	
		return $('#t_square').val('Площадь < 0')}
	const lose = ($('#t_lose').val() === $('#lose_warm').val()) ? 1 : 1.1
	const period = $('#t_period').val()
	if (period < 0) { 
		$('#t_power').html('0')
		$('#t_season').html('0')	
		return $('#t_period').val('Период < 0')}
	const heigth = $('#t_heigth').val()
	if (heigth < 0) { 
		$('#t_power').html('0')
		$('#t_season').html('0')	
		return $('#t_heigth').val('Высота < 0')}
	let region = 0
	if ($('#t_location').val() === 'zone1') {
		region = 1.2
	} else if ($('#t_location').val() === 'zone2') {
		region = 1.1
	} else if ($('#t_location').val() === 'zone3') {
		region = 1
	} else if ($('#t_location').val() === 'zone4') {
		region = 0.9
	} 
	const system = ($('#t_system').val() === $('#system_new').val()) ? 1 : 1.35
	const power = ((square*heigth)/30)*lose*system*region
	const season_power = (power*24*period)/2
	$('#t_power').html(power.toFixed(1))
	$('#t_season').html(season_power.toFixed(2))
}

$(document).ready(function(){
	estimate_power()
	$('.calculator').on('change', function() {
		estimate_power()
	});
})

