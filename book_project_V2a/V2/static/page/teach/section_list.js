xpage = _app.curr_page
//alert(xpage.params);
xpage.ds = {}
xpage.apis = {}
xpage.pages = {}
xpage.views = {}
xpage.actions = {}
xpage.xforms = {}

xpage.init = function(){
	
	xpage.render_page(xpage.views.defaultView,'');	
		
	_app.get('api/author/', function(data){
		//_app.msg(data.authors);
		xpage.ds.authors = data.authors
		xpage.sel_init('#sel_author',xpage.ds.authors,'All Authors-D','_id','author')		
	});

	xpage.ds.categories = [{'id':'F','txt':'Fiction-N'},{'id':'N','txt':'Non-Fiction-N'}]
	xpage.sel_init('#sel_category',xpage.ds.categories,'All Categories-D','id','txt','N')		
		
	xpage.apis.getlist = '/api/book';
	xpage.actions.filter_list();	

	_app.bind('#btnAdd','click',xpage.actions.onAdd);
	_app.bind('#searchBooks','keyup',xpage.actions.onSearch);
}

//////////////////////////////////// Define all the custom events  ////////////////////
xpage.actions.filter_list = function(){
	_filter = '/?author=' + $('#sel_author').val()
	_filter += '&category=' + $('#sel_category').val()
	_app.log(_filter);

	_app.get(xpage.apis.getlist + _filter, function( data ) {	
		_app.log(data);
		_app.curr_page.render_html(xpage.views.tableView,data, 'x-books');
		_app.curr_page.table = _app.curr_page.render_table('#tbl_books');
	});	
}

xpage.actions.onAdd = function(){
	_app.load_page('admin.book_dtl')
	return false;
}

xpage.actions.onEdit = function(id){
	alert('Editing ..' + id);
	_app.load_page('admin.book_dtl')
	return false;
}

xpage.actions.onDelete = function(id){
	alert('Deleting .. ' + id);
	_app.load_page('admin.book_lst')
	return false;
}

xpage.actions.onSearch = function(){
	_app.curr_page.table.search(this.value).draw();
	return false;
}

//////////////////////////////////// Define all the views for the page here  ////////////////////

xpage.views.defaultView = './static/page/book/book_lst.htm'

xpage.views.tableView = `
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
		  <td class="col">{{item._id}}</td>
		  <td class="col">{{item.Date}}</td>
		  <td class="col">{{item.Price}}</td>
		  <td class="col">{{item.author_name}}</td>
		  <td class="col">{{item.BookUrl}}</td>
		  <td class="col">{{item.Desc}}</td>
		  <td class="col">{{item.category_name}}</td>
		  <td class="text-center">
			<button type="button" class="btn btn-danger btn-sm float-end mx-2" 
				onclick='xpage.actions.onDelete("{{item._id}}");'><i class="bi bi-trash"></i> Delete</button>
			<button type="button" class="btn btn-primary btn-sm float-end mx-2" 
				onclick='xpage.actions.onEdit("{{item._id}}");'><i class="bi bi-pencil-square"></i> Edit</button>
		</td>
		</tr>
	  {% endfor %}
	  </tbody>
	</table>	
`

xpage.init();
