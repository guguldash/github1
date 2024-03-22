alert("hi");

$.get( "/api/admin/author/", function( data ) {
	
	$('#author_id').empty();
	$('#author_id').append('<option value="">All Author</option>');

	$.each(data.authors, function () {
		var option = $('<option />');
		option.attr('value', this['_id']).text(this['author_name']);
		$('#author_id').append(option);		 
	});
    $('#author_id').val($('#txtauthor').val())



	if(session_info.curr.sel_author!==undefined && session_info.curr.sel_author!==''){
		$('#author_id').val(session_info.curr.sel_author);
		refbook();
	}			
});

function setauthor(selVal){
	
	session_info.curr.sel_author=selVal.value
	session_info.curr.sel_authorname=selVal.options[selVal.selectedIndex].innerHTML
    refbook();	
}



function setcat(selVal){
	
	session_info.curr.sel_cat=selVal.value
	session_info.curr.sel_catagoriesname=selVal.options[selVal.selectedIndex].innerHTML
    refbook();	
}






function refbook(){
	s="?author="+session_info.curr.sel_author
	s+="&category="+session_info.curr.sel_category
	$.get( "/api/admin/book/"+s, function( data ) {
	
	document.getElementById('lstbook_hdr').innerHTML =  nunjucks.render('./static/pages/book/book_list.htm',data);
	bind_events();
	bindEditEvent();
    
	
	});
}



function bind_events() {
     $('[data-nav]').off().on('click',function(e){
	console.log($(this).data('nav'))
	load_page($(this).data('nav'))
	
	});
	 
    $('[data-do]').off().on('click', function(e) {
        e.preventDefault();
        var action = $(this).data('do');
        var bookId = action.split('book.books.del/')[1];
        console.log("book ID:", bookId);
        deletebook(bookId);
    });

}
function deletebook(bookId) {
    $.ajax({
        url: "/api/admin/book/" + bookId,
        type: "DELETE",
        success: function(response) {
            console.log("novel deleted successfully:", response);
            alert("book deleted successfully!");
            refbook(); 
        },
        error: function(xhr, status, error) {
            console.error("Error deleting novel:", error);
            alert("Error deleting novel. Please try again later.");
        }
    });
}






bind_events();


function bindEditEvent() {
     $('[data-edit]').off().on('click', function(e) {
	console.log($(this).data('edit'));
	id=($(this).data('edit'));

	alert("edit successfully!");
	$.get("/api/admin/book/"+id, function(data) {
	document.getElementById('x-body').innerHTML =  nunjucks.render('./static/pages/book/book_dtl.htm',data);
	$.getScript('/static/pages/book/book_dtl.js')
    });
	});
}

bindEditEvent();





function addbook(){
	s="book.book_det.new"
	document.getElementById('x-body').innerHTML =  nunjucks.render('./static/pages/book/book_dtl.htm','');
	$.getScript('/static/pages/book/book_dtl.js')
}

function init(){
	session_info.curr.sel_author=""
	session_info.curr.sel_cat=""

	
	refbook()
}

init()




