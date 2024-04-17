import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json


class n_book(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    Title: str = Field(...)
    Date: date  = Field(...)
    Price: int  = Field(...)
    category_name: str  = Field(...)
    category_id: str  = Field(...)
    author_name: str  = Field(...)
    author_id: str  = Field(...)
    BookUrl: str  = Field(...)
    Desc: str  = Field(...)
    
    
class n_bookUpdate(BaseModel):
    Title: Optional[str] = None
    Date: Optional[date] = None
    Price: Optional[int] = None
    category: Optional[str] = None
    author_name: Optional[str] = None
    BookUrl: Optional[str] = None
    Desc: Optional[str] = None
