_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './static/page/super_admin/post_lst.htm';
	_cp.api.list = '/api/admin/post/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');	
	
	_cp.data.posts = [{'id':'webpage','txt':'webpage'},{'id':'youtube','txt':'youtube'}]
	_cp.sel_init('#sel_post',_cp.data.posts,'All posts-D','id','txt','')		

	_cp.data.views = _cp.data.views = [{'id':'webpage','txt':'webpage'},{'id':'youtube','txt':'youtube'}]
	_cp.sel_init('#sel_post',_cp.data.posts,'All posts-D','id','txt','')
		

	
	
		
	// Call the filter to get the data.
	_cp.on.filter_list();	

	//Bind events for add and search. 
	//NOTE : Events for edit and delete are defined in their respective onclick events in the view.
	_app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#txtSearch','keyup',_cp.on.Search);
}

// Define all the custom events
_cp.on.filter_list = function(){
    _app.get(_cp.api.list, function( data ) {    
        _app.log(data);
        if ($('#sel_view').val() === 'C'){
            _cp.render_view(_cp.views.cardView,data, 'x-posts');
        }
        else{
            _cp.render_view(_cp.views.tableView,data, 'x-posts');
            _cp.table = _cp.display_table('#tbl_posts');                        
        }
    }); 
}


// _cp.on.Add = function(){
	// _app.nav_page('admin.author_dtl')
	// return false;
// }

_cp.on.Edit = function(id){
	_app.nav_page('super_admin.post_dtl',id)
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
	<table class="table table-sm table-striped" id="tbl_posts">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  <th>Post name</th>
		  <th>Post URL</th>
		  <th>title</th>
		  <th>date</th>
		  <th>description</th> 
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  {% for item in posts %}
		<tr>
		  <td class="col">{{item.post_name}}</td>
		  <td class="col">{{item.post_url}}</td>
		  <td class="col">{{item.title}}</td>
		  <td class="col">{{item.detail}}</td>
		  <td class="col">{{item.description}}</td>

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

