_cp = _app.curr_page

_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './static/page/super_admin/user_lst.htm';
	_cp.api.list = '/api/admin/user/';

	//Render the page.
	_cp.render_page(_cp.views.page,'');	

	//Fill the filter combo boxes.
	_app.get('api/admin/ngo/', function(data){
		//_app.msg(data.authors);
		_cp.data.ngos = data.ngos
		_cp.sel_init('#sel_ngo',_cp.data.ngos,'All ngos-D','_id','ngo_name');
	}); // Missing closing parenthesis here

	_app.get('api/admin/org/', function(data){
		//_app.msg(data.authors);
		_cp.data.orgs = data.orgs
		_cp.sel_init('#sel_org',_cp.data.orgs,'All orgs-D','_id','org_name');		
	}); // Missing closing parenthesis here

	_cp.data.applications = [{'id':'app01','txt':'RehabHub'},{'id':'app02','txt':'HospitalHub'},{'id':'app03','txt':'NutritionHub'},{'id':'app04','txt':'EducationHub'}];
	_cp.sel_init('#sel_app',_cp.data.applications,'All Categories-D','id','txt','');		

	_cp.data.views = [{'id':'app01','txt':'RehabHub'},{'id':'app02','txt':'HospitalHub'},{'id':'app03','txt':'NutritionHub'},{'id':'app04','txt':'EducationHub'}];	
	_cp.sel_init('#sel_app',_cp.data.applications,'All appications-D','id','txt','');

	_cp.data.role = [{'id':'super_admin','txt':'super_admin'},{'id':'admin','txt':'admin'},{'id':'user','txt':'user'},{'id':'staff','txt':'staff'}];
	_cp.sel_init('#sel_role',_cp.data.role,'Select a role','id','txt',':auto');

	_cp.data.views = [{'id':'super_admin','txt':'super_admin'},{'id':'admin','txt':'admin'},{'id':'user','txt':'user'},{'id':'staff','txt':'staff'}];	
	_cp.sel_init('#sel_role',_cp.data.role,'All roles-D','id','txt','');

	// Call the filter to get the data.
	_cp.on.filter_list();	

	// Bind events for add and search. 
	// NOTE: Events for edit and delete are defined in their respective onclick events in the view.
	_app.bind_event('#btnAdd','click',_cp.on.Add);
	_app.bind_event('#txtSearch','keyup',_cp.on.Search);
}


//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.filter_list = function(){
	_filter = '?ngo=' + $('#sel_ngo').val()
	_filter += '&app=' + $('#sel_app').val()
	_filter += '&org=' + $('#sel_org').val()
	_filter += '&role=' + $('#sel_role').val()

	_app.log(_filter);

	_app.get(_cp.api.list + _filter, function( data ) {	
		_app.log(data);
		if ($('#sel_view').val() === 'C'){
			_cp.render_view(_cp.views.cardView,data, 'x-users');
		}
		else{
			_cp.render_view(_cp.views.tableView,data, 'x-users');
			_cp.table = _cp.display_table('#tbl_users');						
		}
	});	
}

_cp.on.Add = function(){
	_app.nav_page('super_admin.user_dtl')
	return false;
}

_cp.on.Edit = function(id){
	_app.nav_page('super_admin.user_dtl',id)
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
	<table class="table table-sm table-striped" id="tbl_users">
	  <!-- <thead class="table-dark"> -->
	  <thead>
		<tr>
		  <th>Name</th>
		  <th>E-mail id</th>
		  <th>Phonenumber</th>
		  <th>Organization</th>
		  <th>Foundation</th>
		  <th>Application</th>
		  <th>Role</th>
		  <th class="text-center">Actions</th>
		</tr>
	  </thead>
	  <tbody>
	  {% for item in users %}
		<tr>
		  <td class="col">{{item.display_name}}</td>
		  <td class="col">{{item.email}}</td>
		  <td class="col">{{item.phnnumber}}</td>
		  <td class="col">{{item.org_name}}</td>
		  <td class="col">{{item.ngo_name}}</td>
		  <td class="col">{{item.app_name}}</td>
		  <td class="col">{{item.role_name}}</td>
		  
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
				<p class="card-title m-0 float-start">{{item.ngo_name}} | {{item.app_name}}</p>
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
