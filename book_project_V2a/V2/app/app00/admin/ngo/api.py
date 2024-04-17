from fastapi import APIRouter, Body, Request, Form, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import uuid
import json
from V2.app.app00.admin.ngo.model import m_ngo,ngoUpdate
 

admin_ngo_api = APIRouter()

#create
@admin_ngo_api.post("/", response_description="Create a new ngo", status_code=status.HTTP_201_CREATED, response_model=m_ngo)
async def create_ngo(request: Request, p_ngo: m_ngo = Body(...)):
    ngo = jsonable_encoder(p_ngo)
    new_ngo = request.app.database["ngos"].insert_one(ngo)
    created_ngo = request.app.database["ngos"].find_one(
        {"_id": new_ngo.inserted_id}
    )
    return created_ngo
    
    
@admin_ngo_api.get("/", response_description="List all ngo")
def list_ngo(request: Request,app:str=''):
    
        # print('app is:',app)
        qry = {}
        
        if 'x-ses' in request.headers:
            # print ('FILTERING ...')
            ses = request.headers['x-ses']        
            j_ctx = json.loads(ses)
            
        if app!='':
            qry['app_id'] = app
            
        ngos = list(request.app.database["ngos"].find(qry))
        # print(ngos)
        return {"ngos":ngos}




#delete
@admin_ngo_api.delete("/{id}", response_description="Delete a ngo")
def delete_ngo(id: str, request: Request, response: Response):
    delete_result = request.app.database["ngos"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ngo with ID {id} not found")


#find
@admin_ngo_api.get("/{id}", response_description="Get a single ngo by id")
def find_ngo(id: str, request: Request):
    if (ngo := request.app.database["ngos"].find_one({"_id": id})) is not None:
        return ngo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ngo with ID {id} not found")
    
    
#UPDATE 
@admin_ngo_api.post("/{id}", response_description="Update a ngo",)
async def update_ngo(id: str, request: Request, ngo: ngoUpdate = Body(...)):
    ngo = {k: v for k, v in ngo.model_dump().items() if v is not None}
    update_result = request.app.database["ngos"].update_one(
        {"_id": id}, {"$set": ngo}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ngo with ID {id} not found")
    if (
        existing_ngo := request.app.database["ngos"].find_one({"_id": id})
    ) is not None:
        return existing_ngo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ngo with ID {id} not found")
  