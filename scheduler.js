//This function is used to download the json file
//Source: https://ourcodeworld.com/articles/read/189/how-to-create-a-file-and-generate-a-download-with-javascript-in-the-browser-without-a-server
function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

$('document').ready(function() {
	//Add new row once input is added
	$('.form').on('change keyup', '.first', function(e) {
		if(e.key != 'Tab' && $(this).parent()[0] === $(this).parents('.form').find('.row:last-child')[0]) {
			var newRow = $(this).parent().clone();
			newRow.find('input').val('');
			$(this).parents('.form').append(newRow);
		}
	});

	//On focusout of the input or select
	$('.form').on('focusout', '.first', function() {
		//Remove if the row is empty and it's not the last row 
		if(!$(this).val() && !$(this).parent().is(':last-child'))
			$(this).parent().remove();

		//Remove the select elements
		var attr = $(this).parent().attr('data-source');
		if((attr == 'shiftType' || attr == 'constraints') && !$(this).parent().is(':last-child') && $(this).val() == $(this).attr('data-default'))
			$(this).parent().remove();
	});

	$('.form').on('change', '[data-source] .first', function() {
		var parent = $(this).parent();
		var section = parent.attr('data-source');

		var sources = $('[data-source=' + section + ']');
		var targets = $('[data-target=' + section + ']');

		var vals = '';
		sources.find('.first').each(function() {
			if($(this).val())
				vals += '<option>' + $(this).val() + '</option>';
		});

		targets.each(function() {
			var str = '';
			if($(this).attr('data-default'))
				str += '<option>' + $(this).attr('data-default') + '</option>';

			str += vals;
			$(this).html(str);
		});
	});

	$('#download-btn').click(function() {
		var settingsObj = {};

		settingsObj.locations = [];
		$('#locations input').each(function() {
			if($(this).val())
				settingsObj.locations.push($(this).val());
		});
		
		settingsObj.personTypes = [];
		$('#personTypes .row').each(function() {
			if($(this).find('.first').val()) {
				var name = $(this).find('.first').val();
				var reqHours = $(this).find('.reqHours').val();
				var location = $(this).find('.locationName').val();
				settingsObj.personTypes.push([name, reqHours, location]);
			}
		});

		settingsObj.people = [];
		$('#people .row').each(function() {
			if($(this).find('.first').val()) {
				var name = $(this).find('.first').val();
				var type = $(this).find('.myType').val();
				var workedHours = $(this).find('.workedHours').val();
				settingsObj.people.push([name, type, workedHours]);
			}
		});	

		settingsObj.shiftTypes = [];
		$('#shiftTypes .row').each(function() {
			var first = $(this).find('.first');
			if(first.val() != first.attr('data-default')) {
				var length = first.val();
				var type = $(this).find('.myType').val();
				var dates = $(this).find('.dates').val();
				settingsObj.shiftTypes.push([length, type, dates]);
			}
		});
		
		download("scheduler_settings.json", JSON.stringify(settingsObj));
	});
});