from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid,json
from V2.app.book.model import n_book, n_bookUpdate

api_book = APIRouter()

#CREATE
@api_book.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=n_book)
async def create_book(request: Request, book: n_book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book
    
#LIST FILTERING  
@api_book.get("/", response_description="List all books")
def list_book(request: Request,author:str='',category:str=''):
    qry = {}
    
    if 'x-ses' in request.headers:
        ses = request.headers['x-ses']        
        j_ctx = json.loads(ses)
        
    if author!='':
        qry['author_id'] = author
        
    if category!='':
        qry['category_id'] = category
        
    books = list(request.app.database["books"].find(qry))
    return {"books":books}
    
    
#LIST 
# @api_book.get("/", response_description="List all books")
# def list_books(request: Request):
    # books = list(request.app.database["books"].find({}))
    # print(books)
    # return {"books":books}
    
    
#DELETE
@api_book.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    delete_result = request.app.database["books"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")
    
#UPDATE
@api_book.post("/{id}", response_description="Update a book", response_model=n_book)
async def update_book(id: str, request: Request, book: n_bookUpdate = Body(...)):
    p = await request.json()
    print(p)
    update_result = request.app.database["books"].update_one(
        {"_id": id}, {"$set": p}
    )
    print(update_result)
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")

    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")
   

#FIND   
@api_book.get("/{id}", response_description="Get a single book by id", response_model=n_book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")


 