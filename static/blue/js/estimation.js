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
	const power = Math.ceil(((square*heigth)/30)*lose*system*region)
	const season_heat = (power*24*period)/2
	$('#t_power').html(power)
	$('#t_season').html(season_heat.toFixed(0))
}

const calculate_fuel = () => {
	const season_heat = $('#t_season').html()
	const wood = (season_heat/4.2/0.7/1000).toFixed(2)
	$('#wood_volume').html(wood + ' м3')
	$('#wood_sum').html(((wood/0.8)*$('#wood_cost').val()).toFixed(2))
	const coal = (season_heat/7.8/1000).toFixed(2)	
	$('#coal_volume').html(coal + ' т')
	$('#coal_sum').html(((coal/0.85)*$('#coal_cost').val()).toFixed(2))
	const browncoal = (season_heat/3.6/1000).toFixed(2) 
	$('#brown_coal_volume').html(browncoal + ' т')
	$('#brown_coal_sum').html(((browncoal/0.8)*$('#brown_coal_cost').val()).toFixed(2))
	const pellets = (season_heat/4.7/1000).toFixed(2)
	$('#pellets_volume').html(pellets + ' т')
	$('#pellets_sum').html(((pellets/0.9)*$('#pellets_cost').val()).toFixed(2))
	const eurobricket = (season_heat/4.9/1000).toFixed(2) 
	$('#eurobricket_volume').html(eurobricket + ' т')
	$('#eurobricket_sum').html(((eurobricket/0.85)*$('#eurobricket_cost').val()).toFixed(2))
	const gas = (season_heat*0.1).toFixed(2)
	$('#gas_volume').html(gas + ' м3')
	$('#gas_sum').html(((gas/0.9)*$('#gas_cost').val()).toFixed(2))
	const electricity = (season_heat*(2/3)).toFixed(2) 
	$('#electricity_volume').html(electricity + ' кВТ*ч')
	$('#electricity_sum').html(((electricity/0.99)*$('#electricity_cost').val()).toFixed(2))
	const diesel = (season_heat/11.9).toFixed(2)
	$('#diesel_volume').html(diesel + ' л')
	$('#diesel_sum').html(((coal/0.9)*$('#diesel_cost').val()).toFixed(2))
}

$(document).ready(function(){
	estimate_power();
	calculate_fuel();
	$('.calculator').on('change', function() {
		estimate_power();
		calculate_fuel();
	});
});


$('#choose_kotel_btn').click(function (e) {
	e.preventDefault();
	var param = 'filter_' + $(this).data('filter-param');
	var power = parseInt($('#t_power').text());
	location.href = $(this).attr('data-catalogue-url') + '?' + param + '=' + (power - 2) + '-' + (power + 2);
});

