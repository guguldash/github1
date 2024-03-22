from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid, json

from app.admin.author.models import  M_author,authorUpdate


admin_author_api = APIRouter()


#create
       
@admin_author_api.post("/", response_description="Create a new author", status_code=status.HTTP_201_CREATED, response_model= M_author)
async def create_author(request: Request, p_author: M_author = Body(...)):
    j_author = jsonable_encoder(p_author)
    #print(patient)
    new_author = request.app.database["authors"].insert_one(j_author)
    created_author = request.app.database["authors"].find_one(
        {"_id": new_author.inserted_id}
    )

    return created_author
      
       
  

#LIST
@admin_author_api.get("/", response_description="List all authors")
def list_authors(request: Request):
    authors= list(request.app.database["authors"].find({}))
    print(authors)
    return {"authors":authors}
      
   
#DELETE   
@admin_author_api.delete("/{id}", response_description="Delete a author")
def delete_author(id: str, request: Request, response: Response):
    delete_result = request.app.database["authors"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
       

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")  


 #find   
@admin_author_api.get("/{id}", response_description="Get a single author by id", response_model=M_author)
def find_author(id: str, request: Request):
    if (author := request.app.database["authors"].find_one({"_id": id})) is not None:
        return author

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")
         
    

#UPDATE 
@admin_author_api.post("/{id}", response_description="Update a author", response_model=M_author)
async def update_author(id: str, request: Request, author: authorUpdate = Body(...)):
    author= await request.json()
    print(author)
    
    # book = {k: v for k, v in book.dict().items() if v is not None}

    #if len(anganbadi) >= 1:
    update_result = request.app.database["authors"].update_one(
        {"_id": id}, {"$set":author}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")

    if (
        existing_author := request.app.database["authors"].find_one({"_id": id})
    ) is not None:
        return existing_author

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")


