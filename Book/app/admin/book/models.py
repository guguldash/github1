import uuid
from uuid import UUID
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class M_book(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    book_url: str  = Field(...)
    publish_date: date = Field(...)
    catagories_id: str = Field(...)
    catagories_name: str = Field(...)
    price: int = Field(...)
    author_id: str = Field(...)
    author_name: str = Field(...)
    status: str = Field(...)
    Desc: str = Field(...)
    
class bookUpdate(BaseModel):
    title: Optional[str]=None 
    book_url: Optional[str]=None
    publish_date : Optional[date]=None
    catagories_name: Optional[str]=None
    price:Optional[int]=None
    author_name:Optional[str]=None
    Desc:Optional[str]=None
    status:Optional[str]=None
    
class bookUpdatestatus(BaseModel):
    status:Optional[str]=None

