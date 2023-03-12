from typing import Optional, List
from beanie import Document, Link

from pydantic import BaseModel, EmailStr
from models.books import Books


class User(Document):
    email: EmailStr 
    password: str  
    # books: Optional[List[Link[Books]]]
    
    class Settings:
        name = "users"
        
class TokenResponse(BaseModel):
    access_token:str  
    token_type:str  
    