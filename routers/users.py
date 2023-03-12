from models.users import User, TokenResponse
from fastapi import HTTPException, Depends, status, APIRouter
from database.connection import Database
from auth.hashing import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from auth.token import create_access_token

user_router = APIRouter(tags=["User"],)

user_database = Database(User)

password_hash = HashPassword()

@user_router.post("/signup")
async def register_user(user:User)->dict:
    user_exist = await User.find_one(User.email==user.email)
    
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email alrady exists.")
    
    hash_password = password_hash.create_hash(user.password)
    user.password = hash_password
    await user_database.save(user)
    
    return {"message":"User was registered successfully."}

@user_router.post("/login", response_model=TokenResponse)
async def login_user(user:OAuth2PasswordRequestForm=Depends())->dict:
    user_exist = await User.find_one(User.email == user.username)
    
    if not user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    if password_hash.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {"access_token":access_token,"token_type":"Bearer"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid")



