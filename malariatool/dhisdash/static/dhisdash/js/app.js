var selectContentArea = function(identifier) {
	var contentAreaSelector = "#section-" + identifier;

	if ( $(contentAreaSelector).length ) {
		$('.content-wrap > section').removeClass('content-current');
		$(contentAreaSelector).addClass('content-current');
		return true;
	} else {
		alert("Not Implemented");
		return false;
	}
};

$(document).ready(function() {

    $('.selectpicker').selectpicker();

	$('.toggle-option').click(function() {
		var toggledOptionIdentifier = $(this).data('identifier');
		var toggledOptionGroup = $(this).data('group');

		var ok = selectContentArea($(this).html().trim().toLowerCase().replace(/ /g, '-'));
		if (ok) {
			$('.toggle-option-'+toggledOptionGroup).removeClass('active');
			$('.toggle-option-'+toggledOptionIdentifier).addClass('active');		
		}
	});

	$('.tab').click(function() {
		if (selectContentArea($(this).data('identifier'))) {
			$('.tab').removeClass('tab-current');
			$(this).addClass('tab-current');
		} else {
			return false;
		}
	});

});
