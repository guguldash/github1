import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_ngo(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    ngo_name: str = Field(...)
    app_id:str= Field(...)
    app_name:str= Field(...)
    ng_invitecode: str = Field(...)
    
class ngoUpdate(BaseModel):
    ngo_name: Optional[str] = None
    app_id: Optional[str] = None
    app_name: Optional[str] = None
    ng_invitecode: Optional[str] = None