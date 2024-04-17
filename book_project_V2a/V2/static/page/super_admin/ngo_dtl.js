_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './static/page/super_admin/ngo_dtl.htm';
	_cp.api.item = '/api/admin/ngo/';
	
	//If params then it is in EDIT mode. Else Add mode.
	if (_cp.params !== ''){
		_app.get(_cp.api.item + _cp.params, function(item_data){
			_cp.render_page(_cp.views.page,item_data);
			_cp.load();					
		});
	}
	else{
		_cp.render_page(_cp.views.page,'');		
		_cp.load();		
	}
	
}
_cp.load = function(){
	
	_cp.data.applications = [{'id':'app01','txt':'RehabHub'},{'id':'app02','txt':'HospitalHub'},{'id':'app03','txt':'NutritionHub'},{'id':'app04','txt':'EducationHub'}]
	_cp.sel_init('#sel_app',_cp.data.applications,'Select a app','id','txt',':auto')
	
	_app.bind_event('#btnCancel','click',_cp.on.Cancel);
	_app.bind_event('#btnSave','click',_cp.on.Save);	
}
//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('super_admin.ngo_lst');
	return false;
}

_cp.on.Save = function(){
	_app.post_form($('#form_book'), _cp.api.item + _cp.params, function(resp){
		_app.nav_page('super_admin.ngo_lst');
	});
	return false;
}

_cp.init();
