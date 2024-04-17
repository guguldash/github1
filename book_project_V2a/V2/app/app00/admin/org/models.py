import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_sys_org(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    org_name: str = Field(...)
    ngo_id:str= Field(...)
    ngo_name:str= Field(...)
    # org_invitecode: str = Field(...)
    
    
class orgUpdate(BaseModel):
    org_name: Optional[str] = None
    # org_invitecode: Optional[str]
    
    




