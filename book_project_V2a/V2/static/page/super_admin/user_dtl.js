_cp = _app.curr_page;

_cp.init = function(){
	_cp.views.page = './static/page/super_admin/user_dtl.htm';
	_cp.api.item = '/api/admin/user/';
	
	//If params then it is in EDIT mode. Else Add mode.
	if (_cp.params !== ''){
		_app.get(_cp.api.item + _cp.params, function(item_data){
			_cp.render_page(_cp.views.page, item_data);
			_cp.load();					
		});
	}
	else{
		_cp.render_page(_cp.views.page, '');		
		_cp.load();		
	}
};

_cp.load = function(){
	_app.get('api/admin/ngo/', function(ngo_data){
		_cp.data.ngos = ngo_data.ngos;
		_cp.sel_init('#sel_ngo', _cp.data.ngos, 'Select an ngo', '_id', 'ngo_name', ':auto');
	}); // Closing parenthesis added here
	
	_app.get('api/admin/org/', function(org_data){
		_cp.data.orgs = org_data.orgs;
		_cp.sel_init('#sel_org', _cp.data.orgs, 'Select an org', '_id', 'org_name', ':auto');
	});
	
	_cp.data.applications = [{'id':'app01','txt':'RehabHub'},{'id':'app02','txt':'HospitalHub'},{'id':'app03','txt':'NutritionHub'},{'id':'app04','txt':'EducationHub'}];
	_cp.sel_init('#sel_app', _cp.data.applications, 'Select an app', 'id', 'txt', ':auto');
	
	_cp.data.role = [{'id':'super_admin','txt':'super_admin'},{'id':'admin','txt':'admin'},{'id':'user','txt':'user'},{'id':'staff','txt':'staff'}];
	_cp.sel_init('#sel_role', _cp.data.role, 'Select a role', 'id', 'txt', ':auto');
	
	_app.bind_event('#btnCancel', 'click', _cp.on.Cancel);
	_app.bind_event('#btnSave', 'click', _cp.on.Save);
};

//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('super_admin.user_lst');
	return false;
};

_cp.on.Save = function(){
	_app.post_form($('#form_book'), _cp.api.item + _cp.params, function(resp){
		_app.msg("save");
		_app.nav_page('super_admin.user_lst');
	});
	return false;
};

_cp.init();
