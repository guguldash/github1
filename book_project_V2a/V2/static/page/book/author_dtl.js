_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './static/page/book/author_dtl.htm';
	_cp.api.item = '/api/author/';
	
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
	
	
	_app.bind_event('#btnCancel','click',_cp.on.Cancel);
	_app.bind_event('#btnSave','click',_cp.on.Save);	
}
//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('admin.author_lst');
	return false;
}

_cp.on.Save = function(){
	_app.post_form($('#author_form'), _cp.api.item + _cp.params, function(resp){
		_app.nav_page('admin.author_lst');
	});
	return false;
}

_cp.init();
