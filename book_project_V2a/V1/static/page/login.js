sessionStorage.removeItem('session_info');
session_info = {"curr":{},"user":{},"page":{}}
reg_info = {}

function doLogIn_web(){
	session_info.curr.device = 'web';
	_data = {'userid': $('#inuserid').val(),'pwd': $('#inpwd').val()};
	_data=JSON.stringify(_data);
	console.log(_data);	
	doLogIn("/web/login/", _data)
}

function doLogIn(_url, _data){	
	$.ajax({
		type: 'POST',
		url: _url,
	    contentType: "application/json; charset=utf-8",
		data: _data,
		success: function(event, response) {
		  console.log(response);
		  on_login(response);
		}.bind(null, event),
		error: function( xhr ) { 
		  alert(xhr.responseJSON.message);
		}
	});	
}

function on_login(resp){
	console.log('FROM LOGIN FUNCTION --------- ', resp);
	
	if (resp.success === false){
		alert(resp.message);
	}
	else {
		session_info.user = resp.data		
		sessionStorage.setItem('session_info', JSON.stringify(session_info));		
		if (resp.data.role === 'admin') x_nav("app.book");			
		if (resp.data.role === 'user') x_nav("app.checkout");	
			 	
	}	
}