import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app00.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]


from app.app00.admin.org.api import admin_org_api as admin_org_apiroutes
app.include_router(admin_org_apiroutes, tags=["orgs"], prefix="/api/admin/org")


#TEST CASE FOR CREATE#
def test_create_org(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_create_org...')
            response = client.post("/api/admin/org/",json={"org_name": "navgurukul","ngo_id":"123","ngo_name":"mairada"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("org_name") == "navgurukul"
            assert body.get("ngo_id") == "123"
            assert body.get("ngo_name") == "mairada"
            # assert body.get("org_invitecode") == "12345"
            assert "_id" in body

# TEST CASE FOR LIST#        
def test_get_list_org(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
        print('test_get_list_org...')
        get_orgs_response = client.get("/api/admin/org/")
        assert get_orgs_response.status_code == 200
        
        
# TEST CASE FOR DELETE#       
def test_delete_org(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
        print('test_delete_org.')
        new_org = client.post("/api/admin/org/", json={"org_name": "navgurukul","ngo_id":"123","ngo_name":"mairada"}).json()
        delete_org_response = client.delete("/api/admin/org/" + new_org.get("_id"))
        assert delete_org_response.status_code == 204
    
    
# TEST CASE FIND#      
def test_get_org(capsys):
    with TestClient(app) as client:
       with capsys.disabled():
        print('test_get_org...')
        new_org = client.post("/api/admin/org/",json={"org_name": "navgurukul","ngo_id":"123","ngo_name":"mairada"}).json()
        get_org_response = client.get("/api/admin/org/" + new_org.get("_id"))
        assert get_org_response.status_code == 200
        # assert get_org_response.json() == new_org
        
      
# TEST CASE FOR UPDATE#       
def test_update_org_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_org_name...')
            new_org = client.post("/api/admin/org/", json={"org_name": "navgurukul","ngo_id":"123","ngo_name":"mairada"}).json()
            response = client.post("/api/admin/org/" + new_org.get("_id"), json={"org_name": "nav-Updated"})
            assert response.status_code == 200
            assert response.json().get("org_name") == "nav-Updated"  

# TEST CASE FOR  NEGATIVE#         
def test_delete_org_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_org_unexisting...')
            delete_org_response = client.delete("/api/admin/org/unexisting_id")
            assert delete_org_response.status_code == 404 
            
# TEST CASE FOR NEGATIVE#        
def test_get_org_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print('test_get_org_unexisting...')
            get_org_response = client.get("/api/admin/org/unexisting_id")
            assert get_org_response.status_code == 404

