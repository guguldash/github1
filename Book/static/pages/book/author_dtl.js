alert('hy');

$('[data-nav]').off().on('click',function(e){
	console.log($(this).data('nav'));
	load_page($(this).data('nav'));

	});



// save for writers

$('[data-do]').off().on('click', function(e) {
	console.log($(this).data('do'))
    id=($(this).data('do'));
    e.preventDefault(); 
    
    var formData = $('#book_form').serializeArray(); 
    
    var postData = {};
    $(formData).each(function(index, obj){
        postData[obj.name] = obj.value;
    });

    $.ajax({
            url: "/api/admin/author/"+id,
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
	document.getElementById('x-body').innerHTML =  nunjucks.render("./static/pages/book/authors.htm",'');
	$.getScript('/static/pages/book/authors.js');

	

    
});