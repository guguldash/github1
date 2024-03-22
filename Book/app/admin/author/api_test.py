from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
import pytest

app = FastAPI()
config = dotenv_values(".env")
app.mongodb_client = MongoClient(config["CONNECTION_STRING"])
app.database = app.mongodb_client[config["DB_NAME"] + "_test"]


app.database["authors"].drop()
#app.mongodb_client.drop_database(config["DB_NAME"] + "_test")

from app.admin.author.api import admin_author_api as admin_author_apiroutes
app.include_router(admin_author_apiroutes, tags=["authors"], prefix="/api/admin/author")


# TEST CASE FOR CREATE#
def test_create_author(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_create_book...')
            response = client.post("/api/admin/author/",json={"author_name":"smita2"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("author_name") == "smita2"
            assert "_id" in body
            
            

#TEST CASE FOR LIST#        
def test_list_get_author():
    with TestClient(app) as client:
        get_authors_response = client.get("/api/admin/author")
        assert get_authors_response.status_code == 200

 
#TEST CASE FOR DELETE#       
def test_delete_author():
    with TestClient(app) as client:
        new_author = client.post("/api/admin/author/", json={"author_name":"smita2"}).json()
        delete_author_response = client.delete("/api/admin/author/" + new_author.get("_id"))
        assert delete_author_response.status_code == 204
           
def test_delete_author_unexisting():
    with TestClient(app) as client:
        delete_author_response = client.delete("/api/admin/author/unexisting_id")
        assert delete_author_response.status_code == 404 
        



#TEST CASE FIND#       
def test_get_author():
    with TestClient(app) as client:
        new_author = client.post("/api/admin/author/", json={"author_name":"smita2"}).json()

        get_author_response = client.get("/api/admin/author/" + new_author.get("_id"))
        assert get_author_response.status_code == 200
        assert get_author_response.json() == new_author
        
def test_get_author_unexisting():
    with TestClient(app) as client:
        get_author_response = client.get("/api/admin/author/unexisting_id")
        assert get_author_response.status_code == 404



def test_update_author_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_author_name')

        new_author = client.post("/api/admin/author/", json={"author_name":"smita2"}).json()
        response = client.post("/api/admin/author/" + new_author.get("_id"), json={"author_name": "smita2-Updated"})
        assert response.status_code == 200
        assert response.json().get("author_name") == "smita2-Updated"            

   
        
