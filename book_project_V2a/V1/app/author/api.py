from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid,json
from V1.app.author.model import n_author, n_authorUpdate

api_author = APIRouter()

#CREATE
@api_author.post("/", response_description="Create a new author", status_code=status.HTTP_201_CREATED, response_model=n_author)
async def create_author(request: Request, author: n_author = Body(...)):
    author = jsonable_encoder(author)
    new_author = request.app.database["authors"].insert_one(author)
    created_author = request.app.database["authors"].find_one(
        {"_id": new_author.inserted_id}
    )

    return created_author
    
#LIST 
@api_author.get("/", response_description="List all authors")
def list_authors(request: Request):
    authors = list(request.app.database["authors"].find({}))
    print(authors)
    return {"authors":authors}
    
#DELETE
@api_author.delete("/{id}", response_description="Delete a author")
def delete_author(id: str, request: Request, response: Response):
    delete_result = request.app.database["authors"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")
    
# update
@api_author.post("/{id}", response_description="Update a author", response_model=n_author)
async def update_author(id: str, request: Request, p: n_authorUpdate = Body(...)):
    p = await request.json()
    print(p)
    update_result = request.app.database["authors"].update_one(
        {"_id": id}, {"$set": p}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")

    if (
        existing_author := request.app.database["authors"].find_one({"_id": id})
    ) is not None:
        return existing_author

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")
   

 # find   
@api_author.get("/{id}", response_description="Get a single author by id", response_model=n_author)
def find_author(id: str, request: Request):
    if (author := request.app.database["authors"].find_one({"_id": id})) is not None:
        return author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"author with ID {id} not found")


 