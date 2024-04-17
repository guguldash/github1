_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './static/page/book/author_lst.htm';
	_cp.api.list = '/api/author/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');	

    // Call the function to fetch and render the list of authors
	_cp.on.filter_list() 
    // Bind events for adding a new author and searching
    // _app.bind_event('#btnAdd','click',_author_page.on.Add);
	_app.bind_event('#txtSearch','keyup',_cp.on.Search);
}

// Define all the custom events
_cp.on.filter_list = function(){
    _app.get(_cp.api.list, function( data ) {    
        _app.log(data);
        if ($('#sel_view').val() === 'C'){
            _cp.render_view(_cp.views.cardView,data, 'x-authors');
        }
        else{
            _cp.render_view(_cp.views.tableView,data, 'x-authors');
            _cp.table = _cp.display_table('#tbl_authors');                        
        }
    }); 
}


// _cp.on.Add = function(){
	// _app.nav_page('admin.author_dtl')
	// return false;
// }

_cp.on.Edit = function(id){
	_app.nav_page('admin.author_dtl',id)
	return false;
}

_cp.on.Delete = function(id){
	_app.del(_cp.api.list + id, function(data){
		_cp.init();
	});
	return false;
}

_cp.on.Search = function(){
	_cp.table.search(this.value).draw();
	return false;
}

_cp.views.tableView = `
	{% import  "static/js/app/macros.htm" as macros with context%}
	<table class="table table-sm table-striped" id="tbl_authors">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  <th>Author</th>
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  {% for item in authors %}
		<tr>
		  
		  <td class="col">{{item.author}}</td>
		  
		  <td class="text-center">
			<button type="button" class="btn btn-danger btn-sm float-end mx-2" 
				onclick='_cp.on.Delete("{{item._id}}");'><i class="bi bi-trash"></i> Delete</button>
			<button type="button" class="btn btn-primary btn-sm float-end mx-2" 
				onclick='_cp.on.Edit("{{item._id}}");'><i class="bi bi-pencil-square"></i> Edit</button>
		</td>
		</tr>
	  {% endfor %}
	  </tbody>
	</table>	
`
_cp.init();

