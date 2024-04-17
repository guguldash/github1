from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid, json,os
from V2.app.app00.admin.org.models import m_sys_org,orgUpdate
from V2.app.main import app as curr_app


admin_org_api = APIRouter()

#create    
@admin_org_api.post("/", response_description="Create a new org", status_code=status.HTTP_201_CREATED, response_model=m_sys_org)
async def create_org(request: Request, p_org: m_sys_org = Body(...)):
    org = jsonable_encoder(p_org)
    org["org_invitecode"]=str(uuid.uuid4())
    new_org = curr_app.database["orgs"].insert_one(org)
    created_org = curr_app.database["orgs"].find_one(
        {"_id": new_org.inserted_id}
    )
    # print(new_org)
    return created_org

#LIST  
@admin_org_api.get("/", response_description="List all org")
def list_org(request: Request,org:str='',ngo:str=''):
    # print('org is:',org)
    # print('ngo is:',ngo)
    qry = {}
    # print("org header:",request.headers)
    

    if 'x-ses' in request.headers:
        # print ('FILTERING org ...')
        ses = request.headers['x-ses']        
        j_ctx = json.loads(ses)
        # print(j_ctx)
    if org!='':
        qry['org_id'] = org
        
    if ngo!='':
        qry['ngo_id'] = ngo
        

    orgs = list(request.app.database["orgs"].find(qry))
    # print(orgs)
    return {"orgs":orgs}
    
   
#DELETE
@admin_org_api.delete("/{p_id}", response_description="Delete a org")
async def delete_org(p_id: str, request: Request, response: Response):
    # print("ORG IS:", p_id)
    delete_result = curr_app.database["orgs"].delete_one({"_id": p_id})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"org with ID {p_id} not found")    
    
    
#FIND
@admin_org_api.get("/{id}", response_description="Get a single org by id")
def find_org(id: str, request: Request):
    if (org := request.app.database["orgs"].find_one({"_id": id})) is not None:
        return org
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"org with ID {id} not found")
    
    
    

    
@admin_org_api.post("/{id}", response_description="Update a org",)
async def update_org(id: str, request: Request, org: orgUpdate = Body(...)):
    p = await request.json()
    print(p)
    update_result = request.app.database["orgs"].update_one(
        {"_id": id}, {"$set": p}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"org with ID {id} not found")

    if (
        existing_org := request.app.database["orgs"].find_one({"_id": id})
    ) is not None:
        return existing_org

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"org with ID {id} not found")
   

