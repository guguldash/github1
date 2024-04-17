x_getJSON( "api/author/", function( data ) {
	$('#author_id').empty();
	$.each(data.authors, function () {
		var option = $('<option/>');
		option.attr('value', this['_id']).text(this['author']);
		$('#author_id').append(option);		 
	});
    $('#author_id').val($('#txtauthor').val())

});

function setauthor(selVal){
	$('#txtauthorname').val(selVal.options[selVal.selectedIndex].innerHTML)
	$('#txtauthor').val(selVal.value)

}	

function setcategory(selVal){
	$('#txtcategoryname').val(selVal.options[selVal.selectedIndex].innerHTML)
	$('#txtcategory').val(selVal.value)

}	

