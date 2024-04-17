let x_routes = {
  // "web.login": {x_page:"./static/page/_common/base.htm?v0.01"},
  
//weblogin page-admin &user
  "web.login": {x_page:"./static/page/login.htm?v0.01",x_code:"/static/page/login.js?v7"},
  
//checkout and return/list button connection  
  "app.checkout":{x_api: "/api/book",x_page:"./static/page/book/usercheckout_lst.htm?v1"},
  "app.return":{x_api: "/api/book",x_page:"./static/page/book/userreturn_lst.htm?v7"},

//book-hdr, add, list, edit connection  
  "app.book": {x_api: "/api/book",x_page:"./static/page/book/book_hdr.htm?v0.01",x_code:"/static/page/book/book_hdr.js?v7"},
  "app.book.new": {x_page:"./static/page/book/book_dtl.htm?v0.01",x_code:"/static/page/book/book_dtl.js?v5"},
  "app.book_list":{x_api: "/api/book",x_page:"./static/page/book/book_lst.htm?v0.01",x_div:"lstbook_hdr"},
  "app.book.edit": {x_api : "/api/book",x_page:"./static/page/book/book_dtl.htm?v0.01",x_code:"/static/page/book/book_dtl.js?v3"},
 
//author-header, add, edit connectin
  "app.author": {x_api: "/api/author",x_page:"./static/page/book/author_lst.htm?v0.02"},
  "app.author.new": {x_page:"./static/page/book/author_dtl.htm?v0.01"},
  "app.author.edit": {x_api : "/api/author",x_page:"./static/page/book/author_dtl.htm"}
  
}

let x_actions = {
  // "login": {x_act:"post",x_do:"/web/login",x_go:"app.book"}
  
// save and delete button coonection
  "app.book.save":{x_act:"post",x_do:"/api/book",x_go:"app.book"},
  "app.book.del": {x_act:"del",x_do:"/api/book",x_go:"app.book"},
  
// save and delete button coonection	
  "app.author.save":{x_act:"post",x_do:"/api/author",x_go:"app.author"},
  "app.author.del": {x_act:"del",x_do:"/api/author",x_go:"app.author"}
  
}