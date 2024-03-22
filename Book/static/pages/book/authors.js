function bind_events() {	
	$('[data-nav]').off().on('click',function(e){
	console.log($(this).data('nav'));
	load_page($(this).data('nav'));



	});
	

}



function bindEditEvent() {
    $('[data-edit]').off().on('click', function(e) {
	console.log($(this).data('edit'));
	id=($(this).data('edit'));

	$.get("/api/admin/author/"+id, function(data) {
	document.getElementById('x-body').innerHTML = nunjucks.render('./static/pages/book/author_dtl.htm', data);
	$.getScript('/static/pages/book/author_dtl.js');
    });
	});
}





// / DEL for voles
function deleteauthor() {
    $('[data-do]').off().on('click', function(e) {
        var authorId = $(this).data('do');
        $.ajax({
            url: "/api/admin/author/" + authorId, 
            type: "DELETE",
            success: function(response) {
                console.log("author deleted successfully:", response);
                alert("author deleted successfully!");
                refauthor(); 
            },
            error: function(xhr, status, error) {
                console.error("Error deleting author:", error);
                alert("Error deleting author. Please try again later.");
            }
        });
    });
}



function refauthor(){
	$.get( "/api/admin/author/", function( data ) {
		
	document.getElementById('x-body').innerHTML =  nunjucks.render("./static/pages/book/authors.htm",data);
	bind_events();
	bindEditEvent();
	deleteauthor();
	
	});

}










function init(){
	
	
	refauthor()
}
init()
