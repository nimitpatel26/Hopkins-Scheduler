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
});