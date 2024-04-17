sessionStorage.removeItem('session_info');
session_info = {"curr":{},"page":{}}

x_getJSON( "api/author/", function( data ) {
	$('#author_id').empty();
    $('#author_id').append('<option value="">All AUTHOR</option>');
	$.each(data.authors, function () {
		var option = $('<option/>');
		option.attr('value', this['_id']).text(this['author']);
		$('#author_id').append(option);		 

	});
    $('#author_id').val($('#txtauthor').val())
	if(session_info.curr.sel_author!==undefined && session_info.curr.sel_author!==''){
		$('#sel_author').val(session_info.curr.sel_author);
		refbook();
	}			

});

//author
function setauthor(selVal){
	$('#txtauthorname').val(selVal.options[selVal.selectedIndex].innerHTML)
	$('#txtauthor').val(selVal.value)
	session_info.curr.sel_author=selVal.value
	session_info.curr.sel_authorname=selVal.options[selVal.selectedIndex].innerHTML
    refbook();
}

//category
function setcategory(selVal){
	// $('#txtcategoryname').val(selVal.options[selVal.selectedIndex].innerHTML)
	// $('#txtcategory').val(selVal.value)
	session_info.curr.sel_category=selVal.value
	session_info.curr.sel_categoryname=selVal.options[selVal.selectedIndex].innerHTML
    refbook();
}

function refbook(){
	// s="app.book_list"
	s="app.book_list/?author="+session_info.curr.sel_author
	s+="&category="+session_info.curr.sel_category
	// alert(s)
	// console.log(s)
	x_load(s);
}

function addbook(){
	s="app.book.new"
	// console.log(s)
	x_load(s);
 }
 
function init(){
	session_info.curr.sel_author=""
	session_info.curr.sel_category=""
	refbook()
	
}
init()
