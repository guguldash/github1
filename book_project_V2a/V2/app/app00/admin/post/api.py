from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
import json
from V2.app.app00.admin.post.model import m_post,postUpdate
from urllib.parse import urlparse
import requests



admin_post_api = APIRouter()

#create
@admin_post_api.post("/", response_description="Create a new post", status_code=status.HTTP_201_CREATED, response_model=m_post)
async def create_post(request: Request, p_post: m_post = Body(...)):
    post = jsonable_encoder(p_post)
    new_post = request.app.database["posts"].insert_one(post)
    created_post = request.app.database["posts"].find_one(
        {"_id": new_post.inserted_id}
    )
    return created_post


#list 
@admin_post_api.get("/", response_description="List all posts")
def list_posts(request: Request):
    posts = list(request.app.database["posts"].find({}))
    print(posts)
    return {"posts":posts}
 
 
  
 #find   
@admin_post_api.get("/{id}", response_description="Get a single post by id", response_model=m_post)
def find_post(id: str, request: Request):
    if (post := request.app.database["posts"].find_one({"_id": id})) is not None:
        return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} not found")
   
 
#delete
@admin_post_api.delete("/{id}", response_description="Delete a post")
def delete_post(id: str, request: Request, response: Response):
    delete_result = request.app.database["posts"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} not found")
    
    
#UPDATE 
@admin_post_api.post("/{id}", response_description="Update a post",)
async def update_post(id: str, request: Request, post: postUpdate = Body(...)):
    post = {k: v for k, v in post.model_dump().items() if v is not None}
    update_result = request.app.database["posts"].update_one(
        {"_id": id}, {"$set": post}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} not found")
    if (
        existing_post := request.app.database["posts"].find_one({"_id": id})
    ) is not None:
        return existing_post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} not found")


 # post details 
@admin_post_api.get("/postdetail/", response_description="post details ")
def details_posts(request: Request,url:str=''):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract site name
    site_name = parsed_url.netloc.split('.')[0]

    # Extract slug name without date
    path_parts = parsed_url.path.strip('/').split('/')
    slug_name = '/'.join(path_parts[3:])

    print("Site Name:", site_name)
    print("Slug Name:", slug_name)

    url =requests.get(
    "https://public-api.wordpress.com/rest/v1.1/sites/"+site_name+".wordpress.com/posts/slug:"+slug_name)
    data=url.json() 
    posts={}
    posts['title']=data['title'] 
    posts['date']=data['date'] 
    posts['excerpt']=data['excerpt'] 



    return {"posts":posts} 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
