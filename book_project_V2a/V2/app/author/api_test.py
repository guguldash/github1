import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient

app = FastAPI()
config = dotenv_values(".env")
app.mongodb_client = MongoClient(config["CONNECTION_STRING"])
app.database = app.mongodb_client[config["DB_NAME"] + "_test"]
app.database["authors"].drop()

from V2.app.author.api import api_author as  author_apiroutes
app.include_router(author_apiroutes, tags=["author"], prefix="/api/author")

#TEST CASE FOR CREATE 
def test_create_author(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_create_author")
            response = client.post("/api/author/", json={"author":"austen"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("author") == "austen"
            
            assert "_id" in body
            
#TEST CASE FOR LIST#       
def test_list_author(capsys):
    with TestClient(app) as client:
         with capsys.disabled():
            print('test_list_author')
            get_authors_response = client.get("/api/author")
            assert get_authors_response.status_code == 200
            
#TEST CASE FOR FIND           
def test_find_author(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_find_author')
            new_author = client.post("/api/author/",json={"author":"austen"}).json()
            response = client.get("/api/author/" + new_author.get("_id"))
            get_author_response = client.get("/api/author")
            assert get_author_response.status_code == 200
           
#TEST CASE FOR DELETE            
def test_delete_author(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_author')
            new_author = client.post("/api/author/",json={"author":"austen"}).json()
            delete_author_response = client.delete("/api/author/" + new_author.get("_id"))
            assert delete_author_response.status_code == 204
                      
# TEST CASE FOR UPDATE NAME
def test_update_author(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_author')
            new_author = client.post("/api/author/",json={"author":"austen"}).json()
            response = client.post("/api/author/" + new_author.get("_id"), json={"author":"austen - Updated"})
            assert response.status_code == 200
            assert response.json().get("author") == "austen - Updated"
           
#TEST CASE FOR negative#
def test_get_author_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print("test_get_author_unexisting...")
            get_author_response = client.get("/api/author/unexisting_id")
            assert get_author_response.status_code == 404