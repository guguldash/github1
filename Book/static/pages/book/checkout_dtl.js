$('[data-nav]').off().on('click',function(e){
	console.log($(this).data('nav'));
	load_page($(this).data('nav'));

	});

