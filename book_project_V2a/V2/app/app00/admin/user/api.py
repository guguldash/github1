from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid, json
from V2.app.app00.admin.user.model import m_sys_user,userUpdate, userUpdateFull
from V2.app.main import app as curr_app

admin_user_api = APIRouter()


#create
@admin_user_api.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=m_sys_user)
async def create_user(request: Request, p_user: m_sys_user = Body(...)):
    user = jsonable_encoder(p_user)
    new_user = curr_app.database["users"].insert_one(user)
    created_user = curr_app.database["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    # print(new_user)
    return created_user
    
#List  
@admin_user_api.get("/", response_description="List all user")
def list_user(request: Request,org:str='',ngo:str='',app:str='',role:str=''):
    # print('org is:',org)
    # print('ngo is:',ngo)
    # print('app is:',app)
    # print('role is:',role)

    qry = {}
    if 'x-ses' in request.headers:
        # print ('FILTERING ...')
        ses = request.headers['x-ses']        
        j_ctx = json.loads(ses)
    if org!='':
        qry['org_id'] = org
        
    if ngo!='':
        qry['ngo_id'] = ngo
        
    if app!='':
        qry['app_id'] = app
        
    if role!='':
        qry['role_id'] = role
    # print("er",qry)
        
    users = list(request.app.database["users"].find(qry))
    # print(users)
    return {"users":users}
    
# def list_user(request: Request,p_role_name: str ="any",p_org_name: str ="any"):
# projects = list(request.app.database["projects"].find({}))
    # p_lang = 'any'
    # p_level = 'L1'
    # qry = {}
    # if (p_role_name != 'any') :
      # qry['role_name'] = p_role_name

    # if (p_org_name != 'any') :
       # qry['org_name'] = p_org_name

    # print ("users00",qry)
    # users = list(request.app.database["users"].find(qry))
    
    # print(users)
    # return {"users":users}

#find
@admin_user_api.get("/{id}", response_description="Get a single user by id")
def find_user(id: str, request: Request):
    if (user := request.app.database["users"].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with ID {id} not found")
   

#delete
@admin_user_api.delete("/{p_id}", response_description="Delete a user")
async def delete_user(p_id: str, request: Request, response: Response):
    # print("USER IS:", p_id)
    delete_result = curr_app.database["users"].delete_one({"_id": p_id})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with ID {p_id} not found")

   
    
@admin_user_api.post("/{id}", response_description="Update a user",)
async def update_user(id: str, request: Request, user: userUpdate = Body(...)):
    p = await request.json()
    print(p)
    update_result = request.app.database["users"].update_one(
        {"_id": id}, {"$set": p}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with ID {id} not found")

    if (
        existing_user := request.app.database["users"].find_one({"_id": id})
    ) is not None:
        return existing_user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with ID {id} not found")
   

