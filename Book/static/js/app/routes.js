  let x_routes = {
  //"route": {x_api: "", x_page:"", x_div:"",x_code:""}
  "web.login": {x_page:"./static/pages/login.htm?v0.02",x_code:"/static/pages/login.js?v5"},				
  "web.page": {x_page:"./static/pages/_common/base.htm?v0.02"},
  "book.books":{x_page:"./static/pages/book/book_hdr.htm?v1",x_code:"/static/pages/book/book_hdr.js?v7"},
  "book.users":{ x_api :"/api/admin/book",x_page:"./static/pages/book/checkout_hdr.htm?v1",x_code:"/static/pages/book/checkout_hdr.js?v9"},
  "book.returns":{x_api :"/api/admin/book/bookusers/abcd",x_page:"./static/pages/book/return.htm?v7"},
  "book.books.edit": {x_api :"/api/admin/book",x_page:"./static/pages/book/book_dtl.htm",x_code:"/static/pages/book/book_dtl.js?v1"},
  "book.list":{x_api: "/api/admin/book",x_page:"./static/pages/book/book_list.htm?v0.01",x_div:"lstbook_hdr"},
  "user.list":{x_api: "/api/admin/book",x_page:"./static/pages/book/checkout_list.htm?v0.01",x_div:"lstuserbook_hdr"},
  "book.book_det.new":{x_page:"./static/pages/book/book_dtl.htm",x_code:"/static/pages/book/book_dtl.js?v1"},
  "author.author_det.new":{x_page:"./static/pages/book/author_dtl.htm"},
  "book.authors": {x_api: "/api/admin/author",x_page:"./static/pages/book/authors.htm"},
  "book.authors.edit": {x_api :"/api/admin/author",x_page:"./static/pages/book/author_dtl.htm"},

  
  
  

}

let x_actions = {
  "admin.book.save":{x_act:"post",x_do:"/api/admin/book",x_go:"book.books"},
  "admin.book.del": {x_act:"del",x_do:"/api/admin/book",x_go:"book.books"},
  "admin.author.del": {x_act:"del",x_do:"/api/admin/author",x_go:"book.authors"},
  "admin.author.save": {x_act:"post",x_do:"/api/admin/author",x_go:"book.authors"},
  "admin.book.checkout":{x_act:"post",x_do:"/api/admin/book",x_go:"book.users"},
  "admin.book.return":{x_act:"post",x_do:"/api/admin/book",x_go:"book.returns"},

  
}