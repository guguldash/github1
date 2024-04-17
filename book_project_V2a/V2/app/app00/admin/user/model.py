import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_sys_user(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    display_name: str = Field(...)
    pwd: str = Field(...)
    email:str= Field(...)
    phnnumber:str= Field(...)
    ngo_id: str = Field(...)
    ngo_name: str = Field(...)    
    app_id:str= Field(...)
    app_name:str= Field(...)
    org_id: str= Field(...)
    org_name:str= Field(...)
    role_id:str= Field(...)
    role_name:str= Field(...)
    
        
class userUpdate(BaseModel):
    display_name: Optional[str] = None
    pwd:  Optional[str] = None
    email:Optional[str] = None
    phnnumber:Optional[str] = None

class userUpdateFull(BaseModel):
    display_name: Optional[str] = None
    pwd:  Optional[str] = None
    email:Optional[str] = None
    phnnumber:Optional[str] = None
    ngo_id: str = Field(...)
    ngo_name: str = Field(...)    
    app_id:str= Field(...)
    app_name:str= Field(...)
    org_id: str= Field(...)
    org_name:str= Field(...)
    role_id:str= Field(...)
    role_name:str= Field(...)
