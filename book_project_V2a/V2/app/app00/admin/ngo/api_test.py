import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app00.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]


from app.app00.admin.ngo.api import admin_ngo_api as admin_ngo_apiroutes
app.include_router(admin_ngo_apiroutes, tags=["ngos"], prefix="/api/admin/ngo")


#TEST CASE FOR CREATE#
def test_create_ngo(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_create_ngo...')
            response = client.post("/api/admin/ngo/",json={"ngo_name": "Myrada","app_id": "02","app_name":"Healthcare Assistance","ng_invitecode":"@ng67"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("ngo_name") == "Myrada"
            assert body.get("app_id") == "02"
            assert body.get("app_name") == "Healthcare Assistance"
            assert body.get("ng_invitecode") == "@ng67"
            
            assert "_id" in body
       
#TEST CASE FOR LIST#        
def test_list_ngo(capsys): 
    with TestClient(app) as client:
      with capsys.disabled(): 
        print('test_list_ngo...')
        get_ngos_response = client.get("/api/admin/ngo/")
        assert get_ngos_response.status_code == 200
       
       
#TEST CASE FOR DELETE#       
def test_delete_ngo(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
        print('test_list_ngo...')
        new_ngo = client.post("/api/admin/ngo/", json={"ngo_name": "Myrada","app_id": "02","app_name":"Healthcare Assistance","ng_invitecode":"@ng67"}).json()
        delete_ngo_response = client.delete("/api/admin/ngo/" + new_ngo.get("_id"))
        assert delete_ngo_response.status_code == 204
    
    
#TEST CASE FIND#       
def test_get_ngo(capsys):
    with TestClient(app) as client:
       with capsys.disabled():  
        print('test_get_ngo...')
        new_ngo = client.post("/api/admin/ngo/", json={"ngo_name": "Myrada","app_id": "02","app_name":"Healthcare Assistance","ng_invitecode":"@ng67"}).json()

        get_ngo_response = client.get("/api/admin/ngo/" + new_ngo.get("_id"))
        assert get_ngo_response.status_code == 200
        assert get_ngo_response.json() == new_ngo
         
#TEST CASE FOR UPDATE#       
def test_update_ngo_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_ngo_name...")
            new_ngo = client.post("/api/admin/ngo/", json={"ngo_name": "Myrada","app_id": "02","app_name":"Healthcare Assistance","ng_invitecode":"@ng67"}).json()
            print(new_ngo.get("_id"))
            response = client.post("/api/admin/ngo/" + str(new_ngo.get("_id")), json={"ngo_name": "Myrada-Updated"})
           
            assert response.status_code == 200
            assert response.json().get("ngo_name") == "Myrada-Updated"            

def test_update_app_id(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_app_id...")
            new_ngo = client.post("/api/admin/ngo/", json={"ngo_name": "Myrada","app_id": "02","app_name":"Healthcare Assistance","ng_invitecode":"@ng67"}).json()
            response = client.post("/api/admin/ngo/" + new_ngo.get("_id"), json={"app_id": "02-Updated"})
            assert response.status_code == 200
            assert response.json().get("app_id") == "02-Updated"            


def test_update_app_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_app_name...")
            new_ngo = client.post("/api/admin/ngo/", json={"ngo_name": "Myrada","app_id": "02","app_name":"Healthcare Assistance","ng_invitecode":"@ng67"}).json()
            response = client.post("/api/admin/ngo/" + new_ngo.get("_id"), json={"app_name": "Healthcare Assistance-Updated"})
            assert response.status_code == 200
            assert response.json().get("app_name") == "Healthcare Assistance-Updated" 


def test_update_ngoinvite(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_ngoinvite...")
            new_user = client.post("/api/admin/ngo/", json={"ngo_name": "Myrada","app_id": "02","app_name":"Healthcare Assistance","ng_invitecode":"@ng67"}).json()
            response = client.post("/api/admin/ngo/" + new_user.get("_id"), json={"ng_invitecode": "@ng67-Updated"})
            assert response.status_code == 200
            assert response.json().get("ng_invitecode") == "@ng67-Updated"            
         
            
 

#testcase for negative
 
def test_delete_ngo_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_ngo_unexisting...')
            delete_ngo_response = client.delete("/api/admin/ngo/unexisting_id")
            assert delete_ngo_response.status_code == 404 

def test_get_ngo_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print("test_get_ngo_unexisting...")
            get_ngo_response = client.get("/api/admin/ngo/unexisting_id")
            assert get_ngo_response.status_code == 404

