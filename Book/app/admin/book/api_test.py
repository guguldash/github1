from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
import pytest

app = FastAPI()
config = dotenv_values(".env")
app.mongodb_client = MongoClient(config["CONNECTION_STRING"])
app.database = app.mongodb_client[config["DB_NAME"] + "_test"]


app.database["books"].drop()
#app.mongodb_client.drop_database(config["DB_NAME"] + "_test")

from app.admin.book.api import admin_book_api as admin_book_apiroutes
app.include_router(admin_book_apiroutes, tags=["books"], prefix="/api/admin/book")

# TEST CASE FOR CREATE#
def test_create_book(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_create_book...')
            response = client.post("/api/admin/book/",json={"status":"a","author_id":"123","catagories_id":"222","title":"english","book_url":"firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk","Desc":"premchndar"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("title") == "english"
            assert body.get("author_id") == "123"
            assert body.get("catagories_id") == "222"
            assert body.get("book_url") == "firtation"
            assert body.get("publish_date") == "2024-02-20"
            assert body.get("price") == 30
            assert body.get("catagories_name") == "gg"
            assert body.get("author_name") == "bookbiopk"
            assert body.get("Desc") == "premchndar"
            assert body.get("status") == "a"
            assert "_id" in body
            
            

#TEST CASE FOR LIST#        
def test__list_get_book():
    with TestClient(app) as client:
        get_books_response = client.get("/api/admin/book")
        assert get_books_response.status_code == 200

 
#TEST CASE FOR DELETE#       
def test_delete_book():
    with TestClient(app) as client:
        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title":"english","book_url":"firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk","Desc":"premchndar"}).json()
        delete_book_response = client.delete("/api/admin/book/" + new_book.get("_id"))
        assert delete_book_response.status_code == 204
           
def test_delete_book_unexisting():
    with TestClient(app) as client:
        delete_book_response = client.delete("/api/admin/book/unexisting_id")
        assert delete_book_response.status_code == 404 
        



#TEST CASE FIND#       
def test_get_book():
    with TestClient(app) as client:
        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title":"english","book_url":"firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk","Desc":"premchndar"}).json()

        get_book_response = client.get("/api/admin/book/" + new_book.get("_id"))
        assert get_book_response.status_code == 200
        assert get_book_response.json() == new_book
        
def test_get_book_unexisting():
    with TestClient(app) as client:
        get_book_response = client.get("/api/admin/book/unexisting_id")
        assert get_book_response.status_code == 404



def test_update_title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_title')

        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title": "english", "book_url": "firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk", "Desc": "premchndar"}).json()
        response = client.post("/api/admin/book/" + new_book.get("_id"), json={"title": "english-Updated"})
        assert response.status_code == 200
        assert response.json().get("title") == "english-Updated"            

   
        
def test_update_book_url(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_url')

        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title": "english", "book_url": "firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk", "Desc": "premchndar"}).json()
        response = client.post("/api/admin/book/" + new_book.get("_id"), json={"book_url": "firtation-Updated"})
        assert response.status_code == 200
        assert response.json().get("book_url") == "firtation-Updated"            

def test_update_publish_date(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_publish_date')

        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title": "english", "book_url": "firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk", "Desc": "premchndar"}).json()
        response = client.post("/api/admin/book/" + new_book.get("_id"), json={"publish_date": "2024-02-21"})
        assert response.status_code == 200
        assert response.json().get("publish_date") == "2024-02-21"           

   
         
       
def test_update_catagories_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_catagories_name')

        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title": "english", "book_url": "firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk", "Desc": "premchndar"}).json()
        response = client.post("/api/admin/book/" + new_book.get("_id"), json={"catagories_name": "gg-Updated"})
        assert response.status_code == 200
        assert response.json().get("catagories_name") == "gg-Updated"            

   
def test_update_price(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_price')

        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title": "english", "book_url": "firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk", "Desc": "premchndar"}).json()
        response = client.post("/api/admin/book/" + new_book.get("_id"), json={"price": 35})
        assert response.status_code == 200
        assert response.json().get("price") == 35            
      

def test_update_author_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_author_name')

        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title": "english", "book_url": "firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk", "Desc": "premchndar"}).json()
        response = client.post("/api/admin/book/" + new_book.get("_id"), json={"author_name": "bookbiopk-Updated"})
        assert response.status_code == 200
        assert response.json().get("author_name") == "bookbiopk-Updated"            

def test_update_Desc(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_Desc')

        new_book = client.post("/api/admin/book/", json={"status":"a","author_id":"123","catagories_id":"222","title": "english", "book_url": "firtation","publish_date":"2024-02-20","catagories_name":"gg","price":30,"author_name":"bookbiopk", "Desc": "premchndar"}).json()
        response = client.post("/api/admin/book/" + new_book.get("_id"), json={"Desc": "premchndar-Updated"})
        assert response.status_code == 200
        assert response.json().get("Desc") == "premchndar-Updated"            
