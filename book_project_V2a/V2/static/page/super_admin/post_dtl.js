_cp = _app.curr_page

_cp.init = function(){
	_cp.views.page = './static/page/super_admin/post_dtl.htm';
	_cp.api.item = '/api/admin/post/';
	
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
	
	_cp.data.post = [{'id':'webpage','txt':'webpage'},{'id':'youtube','txt':'youtube'}]
	_cp.sel_init('#sel_post',_cp.data.post,'Select a post','id','txt',':auto')
	
	_app.bind_event('#btnCancel','click',_cp.on.Cancel);
	_app.bind_event('#btnSave','click',_cp.on.Save);
	_app.bind_event('#btnget','click',_cp.on.get);	
	
}
//////////////////////////////////// Define all the custom events  ////////////////////
_cp.on.Cancel = function(){
	_app.nav_page('super_admin.post_lst');
	return false;
}

_cp.on.Save = function(){
	_app.post_form($('#post_form'), _cp.api.item + _cp.params, function(resp){
		_app.nav_page('super_admin.post_lst');
	});
	return false;
}

_cp.on.get = function(){
	var text1 = $('#txturl').val();

    _app.get(_cp.api.item +"postdetail/?url=" + text1, function(data) {
        console.log(data);
        $('#txttitle').val(data.posts.title);
        $('#txtdate').val(data.posts.date);
        $('#txtdesc').val(data.posts.excerpt);
    });
	return false;

}



_cp.init();
