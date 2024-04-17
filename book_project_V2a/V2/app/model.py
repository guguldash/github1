import uuid
from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field, Json

class my_login(BaseModel):
    pwd: str = Field(...)
    userid: str  = Field(...)
   
# class my_key(BaseModel):
    # key_id: str = Field(...)
    
