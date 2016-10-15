// Hide Others field for Industry and Function
$("#industry-others").css('display', 'none');
$("#function-others").css('display', 'none');

// Set event to show Others field when Others is selected from the Industry dropdown list
// and hide Others field when not selected
$("#select-industry").change(function(){

	var option = $("#select-industry option:selected").text();

	if( option == 'Others' ) {
		$("#industry-others").css('display', 'block');
	} else {
		$("#industry-others").css('display', 'none');
	}

});

// Set event to show Others field when Others is selected from the Function dropdown list
// and hide Others field when not selected
$("#select-function").change(function(){

	var option = $("#select-function option:selected").text();

	if( option == 'Others' ) {
		$("#function-others").css('display', 'block');
	} else {
		$("#function-others").css('display', 'none');
	}
	
});