import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json


class n_author(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    author: str = Field(...)
    
    
class n_authorUpdate(BaseModel):
    author: Optional[str] = None
    