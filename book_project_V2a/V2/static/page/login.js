sessionStorage.removeItem('session_info');
session_info = {"curr":{},"user":{}}

_cp = _app.curr_page


//////  Initialize the page  ////////////////////////////////////////////
_cp.init = function(){
	//Define the page URL and the base API
	_cp.views.page = './static/page/login.htm?a';
	_cp.api.login = '/web/login';

	//Render the page.
	_cp.render_page(_cp.views.page,'');

	//Bind events for login. 	
	_app.bind_event('#btnLogin','click',_cp.on.login);

}

//////  Define all the custom events for the page  /////////////////////
_cp.on.login = function(){
	_app.post_form($('#form_login'), _cp.api.login, function(resp){
		if (resp.success === false){
			alert(resp.message);
		}
		 else {
		// sqession_info = JSON.parse(sessionStorage.getItem('session_info'));
		session_info.user.id=resp.data.userid
		session_info.user.name=resp.data.username


        
		
		if (resp.data.role === 'admin') _app.nav_page("admin.book_lst");
		if (resp.data.role === 'superadmin') _app.nav_page("super_admin.ngo_lst");

		
    }
	
			
	});
	return false;
}

_cp.init();
