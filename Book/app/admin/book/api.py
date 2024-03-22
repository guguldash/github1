from fastapi import  APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
import json
import app as curr_app
from app.admin.book.models import  M_book,bookUpdate,bookUpdatestatus


admin_book_api = APIRouter()

#create
       
@admin_book_api.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model= M_book)
async def create_book(request: Request, p_book: M_book = Body(...)):
    j_book = jsonable_encoder(p_book)
    # print(book)
    new_book = request.app.database["books"].insert_one(j_book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book
    
 
    
    



      
@admin_book_api.get("/", response_description="List all books")
def list_book(request: Request,author:str='',cat:str='',status:str=''):

    qry = {}
    if 'x-ses' in request.headers:
        print ('FILTERING ...')
        ses = request.headers['x-ses']        
        j_ctx = json.loads(ses) 

    if author!='':
        qry['author_id'] = author

    if cat!='':
        qry['catagories_id'] = cat
      
    if status!='':
        qry['status'] = status
      
        
    

    books = list(request.app.database["books"].find(qry))
    return {"books":books}




 
 
 


# LIST
# @admin_book_api.get("/", response_description="List all books")
# def list_books(request: Request):
    # books= list(request.app.database["books"].find({}))
    # print(books)
    # return {"books":books}
      
   
#DELETE   
@admin_book_api.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    delete_result = request.app.database["books"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
       

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")  



 #find   
@admin_book_api.get("/{id}", response_description="Get a single book by id", response_model=M_book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"boook with ID {id} not found")
         
    


#UPDATE 
@admin_book_api.post("/{id}", response_description="Update a book", response_model=M_book)
async def update_book(id: str, request: Request, book: bookUpdate = Body(...)):
    book= await request.json()
    print(book)
    
    # book = {k: v for k, v in book.dict().items() if v is not None}

    #if len(anganbadi) >= 1:
    update_result = request.app.database["books"].update_one(
        {"_id": id}, {"$set":book}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")

    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with ID {id} not found")






# UPDATE STAUS working
@admin_book_api.post("/{id}/status", response_description="Update book status")
async def update_book_status(id: str, request: Request, book_status: bookUpdatestatus = Body(...)):
    db = request.app.database

    new_status = "unavailable" if book_status.status == "available" else "available"

    update_result = db["books"].update_one(
        {"_id": id},
        {"$set": {"status": new_status}}
    )
    created_book = request.app.database["books"].find_one(
                {"_id": id}
            )

    if new_status == "unavailable":
            ses = request.headers['x-ses']
            j_ctx = json.loads(ses)

            user_data = {
                "title": created_book["title"],
                "_id": created_book["_id"],
                "user_id": str(j_ctx['id']),
                "user_name": str(j_ctx['name']),
                "author_id": created_book["author_id"],
                "author_name": created_book["author_name"],
            }

            new_book_user = request.app.database["bookusers"].insert_one(user_data)

            
    else:
         delete_result = request.app.database["bookusers"].delete_one({"_id": id})
       

    return id


@admin_book_api.get("/bookusers/abcd", response_description="List all bookusers")
def list_book_users(request: Request):

    qry = {}
    if 'x-ses' in request.headers:
        # print ('FILTERING  ...')
        ses = request.headers['x-ses']        
        j_ctx = json.loads(ses)
        qry['user_id'] = str(j_ctx['id'])
 

    bookusers = list(request.app.database["bookusers"].find(qry))
    return {"bookusers":bookusers}
