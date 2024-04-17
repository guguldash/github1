import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app00.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]

from app.app00.admin.user.api import admin_user_api as admin_user_apiroutes
app.include_router(admin_user_apiroutes, tags=["users"], prefix="/api/admin/user")        
            
#TEST CASE FOR CREATE#
def test_create_user(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_user...')
            response = client.post("/api/admin/user/",json={"display_name": "sai","pwd":"11","ngo_id":"@12","ngo_name":"appolo","app_id":"67","app_name":"app01","email":"@12e","phnnumber":"566","org_id":"01","org_name":"banglore","role_id":"466","role_name":"app"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("display_name") == "sai"
            assert body.get("pwd") == "11"
            assert body.get("ngo_id") == "@12"
            assert body.get("ngo_name") == "appolo"
            assert body.get("app_id") == "67"
            assert body.get("app_name") == "app01"
            assert body.get("org_id") == "01"
            assert body.get("org_name") == "banglore"
            assert body.get("email") == "@12e"
            assert body.get("phnnumber") == "566"
            assert body.get("role_id") == "466"
            assert body.get("role_name") == "app"
            assert "_id" in body
           
#TEST CASE FOR LIST#        
def test_list_user(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
         print('test_delete_user...')
         get_users_response = client.get("/api/admin/user/")
         assert get_users_response.status_code == 200        
        
        
#TEST CASE FOR DELETE#       
def test_delete_user(capsys):
    with TestClient(app) as client:
       with capsys.disabled():
            print('test_delete_user...')
            new_user = client.post("/api/admin/user/",json={"display_name": "sai","email":"@12e","phnnumber":"566","pwd":"11","ngo_id":"@12","ngo_name":"appolo","app_id":"67","app_name":"app01","org_id":"01","org_name":"banglore","role_id":"466","role_name":"app"}).json()
            delete_user_response = client.delete("/api/admin/user/" + new_user.get("_id"))
            assert delete_user_response.status_code == 204
        
    
#TEST CASE FIND#       
def test_get_user(capsys):
    with TestClient(app) as client:
       with capsys.disabled():
            print('test_get_user...')
            new_user = client.post("/api/admin/user/", json={"display_name": "sai","email":"@12e","phnnumber":"566","pwd":"11","ngo_id":"@12","ngo_name":"appolo","app_id":"67","app_name":"app01","org_id":"01","org_name":"banglore","role_id":"466","role_name":"app"}).json()
            get_user_response = client.get("/api/admin/user/" + new_user.get("_id"))
            assert get_user_response.status_code == 200
            assert get_user_response.json() == new_user            
            
        
#TEST CASE FOR UPDATE#       
def test_update_display_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_display_name...')
            new_user = client.post("/api/admin/user/", json={"display_name": "sai","email":"@12e","phnnumber":"566","pwd":"11","ngo_id":"@12","ngo_name":"appolo","app_id":"67","app_name":"app01","org_id":"01","org_name":"banglore","role_id":"466","role_name":"app"}).json()
            response = client.post("/api/admin/user/" + new_user.get("_id"), json={"display_name": "sai-Updated"})
            assert response.status_code == 200
            assert response.json().get("display_name") == "sai-Updated"            
       
       
#TEST CASE FOR POSITIVE#
def test_update_email(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_email...')
            new_user = client.post("/api/admin/user/", json={"display_name":"sai","email":"@12e","phnnumber":"566","pwd":"11","ngo_id":"@12","ngo_name":"appolo","app_id":"67","app_name":"app01","org_id":"01","org_name":"banglore","role_id":"466","role_name":"app"}).json()
            response = client.post("/api/admin/user/" + new_user.get("_id"), json={"email": "@12e-Updated"})
            assert response.status_code == 200
            assert response.json().get("email") == "@12e-Updated" 

#TEST CASE FOR UPDATE POSITIVE#
def test_update_phnnumber(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_phnnumber...')
            new_user = client.post("/api/admin/user/", json={"display_name": "sai","email":"@12e","phnnumber":"566","pwd":"11","ngo_id":"@12","ngo_name":"appolo","app_id":"67","app_name":"app01","org_id":"01","org_name":"banglore","role_id":"466","role_name":"app"}).json()
            response = client.post("/api/admin/user/" + new_user.get("_id"), json={"phnnumber": "566-Updated"})
            assert response.status_code == 200
            assert response.json().get("phnnumber") == "566-Updated"            
                 
     
#TEST CASE FOR UPDATE POSITIVE#
def test_update_pwd(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_update_pwd...')
            new_user = client.post("/api/admin/user/", json={"display_name": "sai","email":"@12e","phnnumber":"566","pwd":"11","ngo_id":"@12","ngo_name":"appolo","app_id":"67","app_name":"app01","org_id":"01","org_name":"banglore","role_id":"466","role_name":"app"}).json()
            response = client.post("/api/admin/user/" + new_user.get("_id"), json={"pwd": "11-Updated"})
            assert response.status_code == 200
            assert response.json().get("pwd") == "11-Updated"            
     
     
#TEST CASE FOR  NEGATIVE #
def test_delete_user_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('Testing user for negative...')
            delete_user_response = client.delete("/api/admin/user/unexisting_id")
            assert delete_user_response.status_code == 404 


#TEST CASE FOR NEGATIVE #
def test_get_user_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print('test_get_user_unexisting...')
            get_user_response = client.get("/api/admin/user/unexisting_id")
            assert get_user_response.status_code == 404

