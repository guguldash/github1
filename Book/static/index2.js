alert("hi");
sessionStorage.removeItem('session_info');
session_info = {"curr":{},"user":{},"page":{}}
reg_info = {}


function LogIn() {
    var userid = $('#inuserid').val();
    var pwd = $('#inpwd').val();
    var data = JSON.stringify({ 'userid': userid, 'pwd': pwd });

    $.ajax({
        type: 'POST',
        url: '/login/web/',
        contentType: "application/json; charset=utf-8",
        data: data,
        success: function (resp) {
            console.log('FROM LOGIN FUNCTION --------- ', resp);
            if (resp.success === false) {
                alert(resp.message);
            } else {
                 session_info.user.id = resp.data.userid;
                session_info.user.name = resp.data.username;

                if (resp.data.role === 'admin') {
                    document.getElementById('x-body').innerHTML = nunjucks.render('./static/pages/book/book_hdr.htm', "");
                    $.getScript('/static/pages/book/book_hdr.js');
					
                } else if (resp.data.role === 'user') {
				  document.getElementById('x-body').innerHTML = nunjucks.render('./static/pages/book/checkout_hdr.htm', "");
				  $.getScript('/static/pages/book/checkout_hdr.js');

				  

                }
				$('[data-nav]').off().on('click',function(e){
				console.log($(this).data('nav'))
				load_page($(this).data('nav'));
                });
            }
        },
        error: function (xhr) {
            alert(xhr.responseJSON.message);
        }
    });
}
function load_page(R){
	document.getElementById('x-body').innerHTML =  nunjucks.render('./static/pages/book/'+R+'.htm','');
	$.getScript('/static/pages/book/'+R+'.js')
	
}






