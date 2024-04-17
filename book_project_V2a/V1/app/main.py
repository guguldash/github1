from fastapi import FastAPI,Request, Form
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from V1.app.book.model import n_book

from V1.app.model import my_login

config = dotenv_values(".env")

app = FastAPI()
app.mount("/static", StaticFiles(directory="V1/static"), name="static")
app.mongodb_client = MongoClient(config["CONNECTION_STRING"])
app.database = app.mongodb_client[config["DB_NAME"]]

from V1.app.book.api import api_book as  book_apiroutes
app.include_router(book_apiroutes, tags=["book"], prefix="/api/book")

from V1.app.author.api import api_author as  author_apiroutes
app.include_router(author_apiroutes, tags=["author"], prefix="/api/author")

myUsers = {
    'admin@book.app':{'pwd':'admin123','role':'admin'},
    'user@book.app':{'pwd':'user123','role':'user'},
    }
    
@app.get("/")
async def index(request: Request):
  return FileResponse('V1/static/index.htm')
  
    
@app.post("/web/login/")
async def login_web(request: Request,p_login:my_login):
    return do_login (request,p_login.userid,p_login.pwd,'web')
    
def do_login(request,uid, pwd, mode):
        
    if (mode == 'web'):
        user_list=list(request.app.database["users"].find({"email":uid,"pwd":pwd}))
    
    if (len(user_list) == 1):
        return {"success": True,"message": "User","data": user_list[0]}
    elif (len(user_list) == 0):
        return do_login_app(uid, pwd)
    else :
        return {"success": False,"message": "Invalid User Credentials"}
        
def do_login_app(uid, pwd):
    if (uid in myUsers):
        if (myUsers[uid]['pwd'] == pwd):
            return {"success": True,"message": "User","data": myUsers[uid]}
        else:
            return {"success": False,"message": "Invalid Credentials"}
    else: 
        return {"success": False,"message": "Invalid Credentials"}

@app.get("/web/")
async def index(request: Request):
  return FileResponse('V1/static/index.htm')
  
       
