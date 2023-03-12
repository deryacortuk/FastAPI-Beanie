from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from database.connection import Database
from models.books import Books, BookUpdate
from typing import List
from auth.authentication import authenticate

book_database = Database(Books)

book_router = APIRouter(tags=["Book"],)

@book_router.get("/", response_model=List[Books])
async def get_all_books()->List[Books]:
    books = await book_database.get_all()
    return books

@book_router.get("/{id}", response_model=Books)
async def get_book(id:PydanticObjectId)->Books:
    book = await book_database.get(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does not exist")
    return book

@book_router.post("/book")
async def add_book(body:Books, user:str=Depends(authenticate))->dict:
    body.reader = user
    await book_database.save(body)
    return {"message":"Book was added successfully"}

@book_router.put("/{id}", response_model=Books)
async def update_book(id:PydanticObjectId, body:BookUpdate, user:str=Depends(authenticate))->dict:
    book = await book_database.get(id)
    if book.reader != user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not allowed!") 
    book_update = await book_database.update(id, body)
    
    if not book_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book does not exist")
    return book_update
        
 

@book_router.delete("/{id}")
async def delete_book(id:PydanticObjectId, user:str = Depends(authenticate))->dict:
    book_ =await book_database.get(id)
    if book_.reader != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission")
    book = await book_database.delete(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not deleted.")
    return {"message":"Book was deleted successfully."}