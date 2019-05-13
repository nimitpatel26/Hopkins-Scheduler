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
		settingsObj.requestOff = [];
		settingsObj.requestOn = [];
		$('#people .row').each(function() {
			if($(this).find('.first').val()) {
				var name = $(this).find('.first').val();
				var type = $(this).find('.myType').val();
				var workedHours = $(this).find('.workedHours').val();
				settingsObj.people.push([name, type, workedHours]);

				$('#constraints .row').each(function() {
					if($(this).find('.first').val() == name) {
						if($(this).find('.onOff').val() == 'Requests off') {
							if(!settingsObj.requestOff[name])
								settingsObj.requestOff[name] = [];

							settingsObj.requestOff[name].push($(this).find('.constraintDate').val());
						} else {
							if(!settingsObj.requestOn[name])
								settingsObj.requestOn[name] = [];

							settingsObj.requestOn[name].push($(this).find('.constraintDate').val());
						}
					}
				});
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

	$("#upload-btn").click(function() {
		var settingsObj = {};
		try {
			settingsObj = JSON.parse($('#uploadText').val());
		} catch(err) {
			alert('Invalid JSON');
			return;
		}

		for(var i = 0; i < settingsObj.locations.length; ++i) {
			$('#locations .row:last-child input').val(settingsObj.locations[i]);
			$('#locations .row:last-child input').trigger('change');
		}

		for(var i = 0; i < settingsObj.personTypes.length; ++i) {
			$('#personTypes .row:last-child .first').val(settingsObj.personTypes[i][0]);
			$('#personTypes .row:last-child .reqHours').val(settingsObj.personTypes[i][1]);
			$('#personTypes .row:last-child .locationName').val(settingsObj.personTypes[i][2]);
			$('#personTypes .row:last-child .first').trigger('change');
		}

		for(var i = 0; i < settingsObj.people.length; ++i) {
			$('#people .row:last-child .first').val(settingsObj.people[i][0]);
			$('#people .row:last-child .myType').val(settingsObj.people[i][1]);
			$('#people .row:last-child .workedHours').val(settingsObj.people[i][2]);
			$('#people .row:last-child .first').trigger('change');
		}

		for(var i = 0; i < settingsObj.shiftTypes.length; ++i) {
			$('#shiftTypes .row:last-child .first').val(settingsObj.shiftTypes[i][0]);
			$('#shiftTypes .row:last-child .myType').val(settingsObj.shiftTypes[i][1]);
			$('#shiftTypes .row:last-child .dates').val(settingsObj.shiftTypes[i][2]);
			$('#shiftTypes .row:last-child .first').trigger('change');
		}
	});
});