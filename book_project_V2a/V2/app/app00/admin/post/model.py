import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class m_post(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    post_name: str = Field(...)
    post_url : str = Field(...)
    title : str = Field(...)
    detail : str = Field(...)
    description : str = Field(...)
   
class postUpdate(BaseModel):
    post_name: Optional[str] = None
    post_url : Optional[str] = None
    title : Optional[str] = None
    detail : Optional[str] = None
    description : Optional[str] = None
