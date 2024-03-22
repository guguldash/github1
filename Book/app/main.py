import os
from fastapi import FastAPI, Request, Form
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.testclient import TestClient
from app.model import my_login
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


config = dotenv_values(".env")

app = FastAPI()



app.mount("/static", StaticFiles(directory="static"),name="static")
app.mongodb_client = MongoClient(config["CONNECTION_STRING"])
app.database = app.mongodb_client[config["DB_NAME"]]

from app.admin.book.api import admin_book_api as admin_book_apiroutes
app.include_router(admin_book_apiroutes, tags=["books"], prefix="/api/admin/book")


from app.admin.author.api import admin_author_api as admin_author_apiroutes
app.include_router(admin_author_apiroutes, tags=["authors"], prefix="/api/admin/author")

myUsers = {
    'admin00@app00.org':{'pwd':'123','role':'admin',"userid":"123","username":"gugul"},
    'admin00@app001.org':{'pwd':'123','role':'user',"userid":"223","username":"subha"},
    
    }

@app.post("/login/web/")
async def login_web(request: Request,p_login:my_login):
    return do_login (request,p_login.userid,p_login.pwd,'web')
    

def do_login(request,uid, pwd, mode):
    # print (request.app.dbname)
    # print(uid,pwd,mode)
    if (mode == 'web'):
        user_list=list(request.app.database["users"].find({"email":uid,"pwd":pwd}))

   

    if (len(user_list) == 1):
        return {"success": True,"message": "User","data": user_list[0]}
    elif (len(user_list) == 0):
        return do_login_app(uid, pwd)
    else :
        return {"success": False,"message": "Invalid User Credentials"}
        

def do_login_app(uid, pwd):
    # print ('TRYING App Login...')
    if (uid in myUsers):
        if (myUsers[uid]['pwd'] == pwd):
            # print(myUsers[uid]['role_id'])
            return {"success": True,"message": "User","data": myUsers[uid]}
        else:
            return {"success": False,"message": "Invalid Credentials"}
    else: 
        return {"success": False,"message": "Invalid Credentials"}

















@app.get("/")
async def index(request: Request):
  return FileResponse('static/index2.html')

 
 
