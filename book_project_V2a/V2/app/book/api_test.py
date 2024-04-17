import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient

from V2.app.book.api import api_book as api_bookroutes

app = FastAPI()
config = dotenv_values(".env")
app.mongodb_client = MongoClient(config["CONNECTION_STRING"])
app.database = app.mongodb_client[config["DB_NAME"] + "_test"]
app.database["books"].drop()
app.include_router(api_bookroutes, tags=["books"], prefix="/api/book")


#TEST CASE FOR CREATE 
def test_create_book(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print("test_create_book")
            response = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"})
            assert response.status_code == 201
            body = response.json()
            assert body.get("Title") == "English"
            assert body.get("Date") == "2023-01-12"
            assert body.get("Price") == 30
            assert body.get("author_name") == "xyz"
            assert body.get("author_id") == ""
            assert body.get("BookUrl") == "png"
            assert body.get("Desc") == "abc"
            assert body.get("category_name") == "3A"
            assert body.get("category_id") == ""
            assert "_id" in body
           
#TEST CASE FOR LIST#       
def test_list_book(capsys):
    with TestClient(app) as client:
         with capsys.disabled():
            print('test_list_book')
            get_books_response = client.get("/api/book")
            assert get_books_response.status_code == 200
          
#TEST CASE FOR FIND           
def test_find_book(capsys):
    with TestClient(app) as client:
        with capsys.disabled(): 
            print('test_find_book')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.get("/api/book/" + new_book.get("_id"))
            # response = client.get("/api/book")
            assert response.status_code == 200
                    
#TEST CASE FOR DELETE            
def test_delete_book(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_delete_book')
            new_book = client.post("/api/book/",json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            delete_book_response = client.delete("/api/book/" + new_book.get("_id"))
            assert delete_book_response.status_code == 204
           
#TEST CASE FOR UPDATE TITLE
def test_update_book_Title(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_Title')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"Title":"science - Updated"})
            assert response.status_code == 200
            assert response.json().get("Title") == "science - Updated"
            
#TEST CASE FOR UPDATE DATE           
def test_update_book_date(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_date')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"Date":"2023-01-13"})
            assert response.status_code == 200
            assert response.json().get("Date") == "2023-01-13"
          
#TEST CASE FOR UPDATE PRICE          
def test_update_book_Price(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_Price')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"Price":35})
            assert response.status_code == 200
            assert response.json().get("Price") == 35
          
#TEST CASE FOR UPDATE CATEGORY         
def test_update_book_category(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_category')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"category_name":"3b - Updated"})
            assert response.status_code == 200
            assert response.json().get("category_name") == "3b - Updated"
            
#TEST CASE FOR UPDATE CATEGORY ID         
def test_update_book_category_id(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_category_id')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"category_id":" - Updated"})
            assert response.status_code == 200
            assert response.json().get("category_id") == " - Updated"
            
#TEST CASE FOR UPDATE AUTHOR NAME           
def test_update_book_author_name(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_author_name')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"author_name":"austean - Updated"})
            assert response.status_code == 200
            assert response.json().get("author_name") == "austean - Updated"
           
#TEST CASE FOR UPDATE AUTHOR ID            
def test_update_book_author_id(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_author_id')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"author_id":" - Updated"})
            assert response.status_code == 200
            assert response.json().get("author_id") == " - Updated"
          
#TEST CASE FOR UPDATE BookUrl            
def test_update_book_bookurl(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_bookurl')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"BookUrl":"jpg- Updated"})
            assert response.status_code == 200
            assert response.json().get("BookUrl") == "jpg- Updated"
            
#TEST CASE FOR UPDATE BookUrl            
def test_update_book_Desc(capsys):
    with TestClient(app) as client:
        with capsys.disabled():
            print('test_update_book_Desc')
            new_book = client.post("/api/book/", json={"Title":"English","Date":"2023-01-12","Price":30,"category_name":"3A","category_id":"","author_name":"xyz","author_id":"","BookUrl":"png","Desc":"abc"}).json()
            response = client.post("/api/book/" + new_book.get("_id"), json={"Desc":"xyz- Updated"})
            assert response.status_code == 200
            assert response.json().get("Desc") == "xyz- Updated"
       
#TEST CASE FOR NEGATIVE
def test_get_bokk_unexisting(capsys):
   with TestClient(app) as client:
        with capsys.disabled():
            print("test_get_book_unexisting...")
            get_book_response = client.get("/api/book/unexisting_id")
            assert get_book_response.status_code == 404
