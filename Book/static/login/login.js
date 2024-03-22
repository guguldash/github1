sessionStorage.removeItem('session_info');
session_info = {"curr":{},"user":{},"page":{}}
reg_info = {}
;

function show_info(type){
	if (type === 'key'){
		$('#key').show();		
		$('#ph').hide();
		$('#otp').hide();
	}

	if (type === 'ph'){
		$('#key').hide();		
		$('#ph').show();
		$('#otp').hide();
	}

	if (type === 'otp'){
		$('#key').hide();		
		$('#ph').hide();
		$('#otp').show();
	}

}

function reg_key(){
	_data = {'key_id': $('#key_id').val()};
	_data=JSON.stringify(_data);
	console.log(_data);	
	
	$.ajax({
		type: 'POST',
		url: 'http://localhost:23905/login/web/',
	    contentType: "application/json; charset=utf-8",
		data: _data,
		success: function(event, response) {
		  console.log(response);
		  reg_entity(response);
		}.bind(null, event),
		error: function( xhr ) { // display ajax errors
		  alert(xhr.responseJSON.message);
		}
	});
}

f

function doLogIn_web(){
	session_info.curr.device = 'web';
	_data = {'userid': $('#inuserid').val(),'pwd': $('#inpwd').val()};
	_data=JSON.stringify(_data);
	console.log(_data);	
	doLogIn("/login/web/", _data)
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
		error: function( xhr ) { // display ajax errors
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
		//session_info.user = resp.data
		
		
		session_info.user.id=resp.data._id
		session_info.user.name=resp.data.display_name

		session_info.user.role_id=resp.data.role_id
		session_info.user.role_name=resp.data.role_name

		

		sessionStorage.setItem('session_info', JSON.stringify(session_info));
		
		//window.location.href = "/" + resp.data.app_id + "/" + session_info.curr.device + "/"
		
		