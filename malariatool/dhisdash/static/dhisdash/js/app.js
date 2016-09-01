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

var tabToggleMap = {};
var activeTab;

$(document).ready(function() {

    $('.selectpicker').selectpicker();

	$('.toggle-option').click(function() {
		var toggledOptionIdentifier = $(this).data('identifier');
		var toggledOptionGroup = $(this).data('group');
		var targetContentArea = $(this).html().trim().toLowerCase().replace(/ /g, '-');

		tabToggleMap[activeTab] = targetContentArea;
		var ok = selectContentArea(targetContentArea);
		if (ok) {
			$('.toggle-option-'+toggledOptionGroup).removeClass('active');
			$('.toggle-option-'+toggledOptionIdentifier).addClass('active');		
		}
	});

	$('.tab').click(function() {
		var targetContentArea = $(this).data('identifier');
		var tabId = $(this).data('identifier');
		console.log(tabId);

		if (tabId == activeTab) {
			return false;
		}

		if ((tabId in tabToggleMap) && (tabToggleMap[tabId] != undefined) ) {
			targetContentArea = tabToggleMap[tabId];
		}

		if (selectContentArea(targetContentArea)) {
			$('.tab').removeClass('tab-current');
			$(this).addClass('tab-current');
			activeTab = tabId;
		} else {
			return false;
		}
	});

});
