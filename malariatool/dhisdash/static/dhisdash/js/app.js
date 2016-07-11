var selectContentArea = function(identifier) {
	var contentAreaSelector = "#section-" + identifier;
	$('.content-wrap > section').removeClass('content-current');
	$(contentAreaSelector).addClass('content-current');
};

$(document).ready(function() {

    $('.selectpicker').selectpicker();

	$('.toggle-option').click(function() {
		var toggledOptionIdentifier = $(this).data('identifier');
		var toggledOptionGroup = $(this).data('group');

		selectContentArea($(this).html().trim().toLowerCase().replace(/ /g, '-'));

		$('.toggle-option-'+toggledOptionGroup).removeClass('active');
		$('.toggle-option-'+toggledOptionIdentifier).addClass('active');		
	
	});

	$('.tab').click(function() {
		$('.tab').removeClass('tab-current');
		$(this).addClass('tab-current');

		selectContentArea($(this).data('identifier'));
	});

});
