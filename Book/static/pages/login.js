sessionStorage.removeItem('session_info');
session_info = {"curr":{},"user":{}}



function doLogIn_web(){
	session_info.curr.device = 'login';
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

function on_login(resp) {
    console.log('FROM LOGIN FUNCTION --------- ', resp);
    
    if (resp.success === false) {
        alert(resp.message);
    } else {
		// sqession_info = JSON.parse(sessionStorage.getItem('session_info'));
		session_info.user.id=resp.data.userid
		session_info.user.name=resp.data.username


        // session_info.curr = resp.data;
		// sessionStorage.setItem('session_info', JSON.stringify(session_info));
		
		// window.location.href = "/" + resp.data.role + "/" + session_info.curr.device + "/"
		
		// if (resp.data.role === 'admin') window.location.href = "/login/?rt=book.books";
		if (resp.data.role === 'admin') x_nav("book.books");
		if (resp.data.role === 'user') x_nav("book.users");

		
    }
	

}