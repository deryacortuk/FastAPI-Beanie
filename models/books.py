from beanie import Document
from typing import Optional, List
from pydantic import BaseModel


class Books(Document):
    title: str  
    author: str 
    description: str  
    tags: List[str]
    reader:Optional[str]
   
    
    class Config:
        schema_extra = {
            "example": {
                "title":"FastAPI",
                "author":"Python",
                "description":"FastAPI Book",
                "tags":["python","fastapi"],
                "reader":"user@example.com",
                
            }
        }
    class Settings: 
        name = "books"
        
        
class BookUpdate(BaseModel):
    title: str  
    author: str 
    description: str 
    tags: Optional[List[str]]
    reader:Optional[str]
    
    class Config:
        schema_extra = {
            "example": {
                "title":"FastAPI",
                "author":"Python",
                "description":"FastAPI Book",
                "tags":["python","fastapi"],
                "reader":"user@example.com",
              
            }
        }

    
    
    