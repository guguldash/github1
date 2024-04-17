_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './static/page/book/book_dtl.htm';
	_cp.api.item = '/api/book/';
	
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
	_app.get('api/author/', function(auth_data){
		_cp.data.authors = auth_data.authors
		_cp.sel_init('#sel_author',_cp.data.authors,'Select an author','_id','author',':auto')		
	});
	
	_cp.data.categories = [{'id':'F','txt':'Fiction-N'},{'id':'N','txt':'Non-Fiction-N'}]
	_cp.sel_init('#sel_category',_cp.data.categories,'Select a category','id','txt',':auto')
	
	_app.bind_event('#btnCancel','click',_cp.on.Cancel);
	_app.bind_event('#btnSave','click',_cp.on.Save);	
}
//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('admin.book_lst');
	return false;
}

_cp.on.Save = function(){
	_app.post_form($('#form_book'), _cp.api.item + _cp.params, function(resp){
		_app.msg("save")
		_app.nav_page('admin.book_lst');
	
	});
	return false;
}

_cp.init();
