_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './static/page/super_admin/org_lst.htm';
	_cp.api.list = '/api/admin/org/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');


	
	_app.get('api/admin/ngo/', function(data){
		//_app.msg(data.authors);
		_cp.data.ngos = data.ngos
		_cp.sel_init('#sel_ngo',_cp.data.ngos,'All ngos-D','_id','ngo_name')		
	});

	

		
	// Call the filter to get the data.
	_cp.on.filter_list();	

	//Bind events for add and search. 
	//NOTE : Events for edit and delete are defined in their respective onclick events in the view.
	_app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#txtSearch','keyup',_cp.on.Search);
}




// Assuming cp.on.filter_list function is defined
_cp.on.filter_list = function() {
	_filter = '?ngo=' + $('#sel_ngo').val()
    _app.log(_filter);

    _app.get(_cp.api.list + _filter, function(data) {
        _app.log(data);
        if ($('#sel_view').val() === 'C') {
            _cp.render_view(_cp.views.cardView, data, 'x-orgs');
        } else {
            _cp.render_view(_cp.views.tableView, data, 'x-orgs');
            _cp.table = _cp.display_table('#tbl_orgs');
        }
    });
};











_cp.on.Add = function(){
	_app.nav_page('super_admin.org_dtl')
	return false;
}

_cp.on.Edit = function(id){
	_app.nav_page('super_admin.org_dtl',id)
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
	<table class="table table-sm table-striped" id="tbl_orgs">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  <th>ORG Name</th>
		  <th>NGO NAME</th>
		  <th>Inivitedcode</th>


		  
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  {% for item in orgs %}
	  
		<tr>
		  
		  <td class="col">{{item.org_name}}</td>
		  <td class="col">{{item.ngo_name}}</td>
		  <td class="col">{{item.org_invitecode}}</td>


		  
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

//////////////////////////////////// Call Current Page Init  ////////////////////

_cp.init();
