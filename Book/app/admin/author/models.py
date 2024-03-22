import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class M_author(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    author_name: str = Field(...)
    
class authorUpdate(BaseModel):
    author_name: Optional[str]
    