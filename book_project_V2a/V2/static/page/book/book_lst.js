_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './static/page/book/book_lst.htm';
	_cp.api.list = '/api/book/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');	

	//Fill the filter combo boxes.
	_app.get('api/author/', function(data){
		//_app.msg(data.authors);
		_cp.data.authors = data.authors
		_cp.sel_init('#sel_author',_cp.data.authors,'All Authors-D','_id','author')		
	});

	_cp.data.categories = [{'id':'F','txt':'Fiction-N'},{'id':'N','txt':'Non-Fiction-N'}]
	_cp.sel_init('#sel_category',_cp.data.categories,'All Categories-D','id','txt','')		

	_cp.data.views = [{'id':'F','txt':'Fiction-N'},{'id':'N','txt':'Non-Fiction-N'}]
	_cp.sel_init('#sel_category',_cp.data.categories,'All Categories-D','id','txt','')		
		
	//Call the filter to get the data.
	_cp.on.filter_list();	

	//Bind events for add and search. 
	//NOTE : Events for edit and delete are defined in their respective onclick events in the view.
	// _app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#txtSearch','keyup',_cp.on.Search);
}

//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.filter_list = function(){
	_filter = '?author=' + $('#sel_author').val()
	_filter += '&category=' + $('#sel_category').val()
	_app.log(_filter);

	_app.get(_cp.api.list + _filter, function( data ) {	
		_app.log(data);
		if ($('#sel_view').val() === 'C'){
			_cp.render_view(_cp.views.cardView,data, 'x-books');
		}
		else{
			_cp.render_view(_cp.views.tableView,data, 'x-books');
			_cp.table = _cp.display_table('#tbl_books');						
		}
	});	
}

_cp.on.Add = function(){
	_app.nav_page('admin.book_dtl')
	return false;
}

_cp.on.Edit = function(id){
	_app.nav_page('admin.book_dtl',id)
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




//////////////////////////////////// Define all the views for the page here  ////////////////////

_cp.views.tableView = `
	{% import  "static/js/app/macros.htm" as macros with context%}
	<table class="table table-sm table-striped" id="tbl_books">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  <th>Title</th>
		  <th>Start Date</th>
		  <th>Price</th>
		  <th>Author</th>
		  <th>BookUrl</th>
		  <th>Desc</th>
		  <th>Category</th>
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  {% for item in books %}
		<tr>
		  <td class="col">{{item.Title}}</td>
		  <td class="col">{{item.Date}}</td>
		  <td class="col">{{item.Price}}</td>
		  <td class="col">{{item.author_name}}</td>
		  <td class="col">{{item.BookUrl}}</td>
		  <td class="col">{{item.Desc}}</td>
		  <td class="col">{{item.category_name}}</td>
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

_cp.views.cardView = `
	{% import  "static/js/app/macros.htm" as macros with context%}
	<div class="row py-0 mt-0">
	{% for item in books %}
		<div class="col-3 p-2">
			<div class="card border-success">
			  <div class="card  -header bg-transparent border-success py-0 px-2">
				<h5 class="card-title m-0">{{item.Title}}</h5>			  
				<p class="card-title m-0 float-start">{{item.author_name}} | {{item.category_name}}</p>
			  </div>
			  <div class="card-body px-2 py-0 m-0">
				<p style="display: block;text-overflow: ellipsis;overflow: hidden;max-height: 5.2em;line-height: 1.8em;">{{item.Desc}}</p>
			  </div>
			  <div class="card-footer border-success m-0">
				<button type="button" class="btn btn-danger btn-sm float-end mx-2" 
					onclick='_cp.on.Delete("{{item._id}}");'><i class="bi bi-trash"></i> Delete</button>
				<button type="button" class="btn btn-primary btn-sm float-end mx-2" 
					onclick='_cp.on.Edit("{{item._id}}");'><i class="bi bi-pencil-square"></i> Edit</button>

			 </div>
			</div>	
		</div>
	  {% endfor %}
	</div>
	
`

//////////////////////////////////// Call Current Page Init  ////////////////////

_cp.init();
