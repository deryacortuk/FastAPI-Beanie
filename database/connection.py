from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic import BaseSettings, BaseModel
from models import books, users

# MONGO_HOST = "127.0.0.1"
# MONGO_USER = "beanie"
# MONGO_PASS = 'beanie'
# MONGO_DB = "beanie_db"

class Settings(BaseSettings):
    # DATABASE_URL= f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/{MONGO_DB}"
    DATABASE_URL = "mongodb://127.0.0.1:27017/Benie"
    SECRET_KEY = "EWGWAUU23922766633"
    
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),document_models=[books.Books, users.User])
        
    # class Config:
    #     env_file = ".env"
        
class Database:
    def __init__(self, model):
        self.model = model 
        
    async def save(self, document)->None:
        await document.create()
        return
    
    async def get(self, id:PydanticObjectId)->Any:
        
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    
    async def get_all(self)->List[Any]:
        docs = await self.model.find_all().to_list()
        return docs
    async def update(self, id:PydanticObjectId, body:BaseModel)->Any:
        doc_id = id 
        desc_body = body.dict()
        desc_body = {k:v for k, v in desc_body.items() if v is not None}
        
        update_query = {"$set":{
            field: value for field, value in desc_body.items()
        }}
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
        
    async def delete(self, id:PydanticObjectId)-> bool:
        doc = await self.get(id)
        if not doc:
            return False
        
        await doc.delete()
        return True