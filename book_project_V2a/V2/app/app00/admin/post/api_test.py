import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from app.app00.main import app

config = dotenv_values(".env")
app.database = app.mongodb_client[app.dbname + "_test"]


from app.app00.admin.post.api import admin_post_api as admin_post_apiroutes
app.include_router(admin_post_apiroutes, tags=["posts"], prefix="/api/admin/post")


#TEST CASE FOR CREATE#
def test_create_post(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_create_post...')
            response = client.post("/api/admin/post/",json={"post_name": "Mediapost","post_url":"Socail post","title":"meta","detail":"xyz","description":"yotube"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("post_name") == "Mediapost"
            assert body.get("post_url") == "Socail post"
            assert body.get("title") == "meta"
            assert body.get("detail") == "xyz"
            assert body.get("description") == "yotube"
            
            assert "_id" in body
       
       
#TEST CASE FOR LIST#        
def test_list_post(capsys): 
    with TestClient(app) as client:
      with capsys.disabled(): 
        print('test_list_post...')
        get_posts_response = client.get("/api/admin/post/")
        assert get_posts_response.status_code == 200
       

#TEST CASE FIND#       
def test_get_post(capsys):
    with TestClient(app) as client:
       with capsys.disabled():  
        print('test_get_post...')
        new_post = client.post("/api/admin/post/", json={"post_name": "Mediapost","post_url":"Socail post","title":"meta","detail":"xyz","description":"yotube"}).json()

        get_post_response = client.get("/api/admin/post/" + new_post.get("_id"))
        assert get_post_response.status_code == 200
        assert get_post_response.json() == new_post
         
         
#TEST CASE FOR DELETE#       
def test_delete_post(capsys):
    with TestClient(app) as client:
      with capsys.disabled():
        print('test_list_post...')
        new_post = client.post("/api/admin/post/", json={"post_name": "Mediapost","post_url":"Socail post","title":"meta","detail":"xyz","description":"A ot Z"}).json()
        delete_post_response = client.delete("/api/admin/post/" + new_post.get("_id"))
        assert delete_post_response.status_code == 204
    
    
#TEST CASE FOR UPDATE#       
def test_update_post_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_post_name...")
            new_post = client.post("/api/admin/post/", json={"post_name": "Mediapost","post_url":"Socail post","title":"meta","detail":"xyz","description":"A ot Z"}).json()
            print(new_post.get("_id"))
            response = client.post("/api/admin/post/" + str(new_post.get("_id")), json={"post_name": "Mediapost-Updated"})
           
            assert response.status_code == 200
            assert response.json().get("post_name") == "Mediapost-Updated"            


#TEST CASE FOR POST_NAME#       
def test_update_post_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_update_post_name...")
            new_post = client.post("/api/admin/post/", json={"post_name": "Mediapost","post_url":"Socail post","title":"meta","detail":"xyz","description":"A ot Z"}).json()
            response = client.post("/api/admin/post/" + new_post.get("_id"), json={"post_name": "Mediapost-Updated"})
            assert response.status_code == 200
            assert response.json().get("post_name") == "Mediapost-Updated" 


#TEST CASE FOR URL#       
def test_update_post_url(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            # print("test_update_post_url...")
            new_post = client.post("/api/admin/post/", json={"post_name": "Mediapost","post_url":"Socail post","title":"meta","detail":"xyz","description":"A ot Z"}).json()
            response = client.post("/api/admin/post/" + new_post.get("_id"), json={"post_name": "url-Updated"})
            assert response.status_code == 200
            assert response.json().get("post_name") == "url-Updated" 


#TEST CASE FOR negative#
def test_delete_post_unexisting(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_post_unexisting...')
            delete_post_response = client.delete("/api/admin/post/unexisting_id")
            assert delete_post_response.status_code == 404 



#TEST CASE FOR negative#
def test_get_post_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print("test_get_post_unexisting...")
            get_post_response = client.get("/api/admin/post/unexisting_id")
            assert get_post_response.status_code == 404

