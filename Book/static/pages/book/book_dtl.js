$.get( "/api/admin/author/", function( data ) {
	
	$('#author_id').empty();
	$.each(data.authors, function () {
		var option = $('<option />');
		option.attr('value', this['_id']).text(this['author_name']);
		$('#author_id').append(option);		 
	});
    $('#author_id').val($('#txtauthor').val())

});

function setauthor(selVal){
	//alert(selVal.value + ' : ' + selVal.options[selVal.selectedIndex].innerHTML);
	$('#txtauthorname').val(selVal.options[selVal.selectedIndex].innerHTML)
	$('#txtauthor').val(selVal.value)
}


function setcat(selVal){
	$('#txtcatagoriesname').val(selVal.options[selVal.selectedIndex].innerHTML);
	$('#txtcat').val(selVal.value);

}
$('#catagories_id').val($('#txtcat').val())

function setstatus(selVal){
	$('#txtstatusname').val(selVal.options[selVal.selectedIndex].innerHTML);
	$('#txtstatus').val(selVal.value);

}
 $('#status_id').val($('#txtstatus').val())


$('[data-nav]').off().on('click',function(e){
	console.log($(this).data('nav'))
	
	document.getElementById('x-body').innerHTML =  nunjucks.render('./static/pages/book/book_hdr.htm','');
	$.getScript('/static/pages/book/book_hdr.js');
	});
	
	
$('[data-do]').off().on('click',function(e){
	console.log($(this).data('do'))
	
	document.getElementById('x-body').innerHTML =  nunjucks.render('./static/pages/book/book_hdr.htm','');
	$.getScript('/static/pages/book/book_hdr.js');
	});

$('[data-do]').off().on('click', function(e) {
	console.log($(this).data('do'))
	id=($(this).data('do'))

    e.preventDefault(); 
    
    var formData = $('#book_form').serializeArray(); 
    
    var postData = {};
    $(formData).each(function(index, obj){
        postData[obj.name] = obj.value;

    });
	

    $.ajax({
        url: "/api/admin/book/" +id,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(postData),
        success: function(response) {
            console.log("Details saved successfully:", response);
            alert("Details saved successfully!");
        },
        error: function(xhr, status, error) {
            console.error("Error saving details:", error);
            alert("Error saving details. Please try again later.");
        }
    });

    document.getElementById('x-body').innerHTML = nunjucks.render('./static/pages/book/book_hdr.htm', '');
    $.getScript('/static/pages/book/book_hdr.js');
});

$('[data-nav]').off().on('click',function(e){
console.log($(this).data('nav'))
load_page($(this).data('nav'));
});
$('#selcatagory').val($('#txtcatagory').val())








