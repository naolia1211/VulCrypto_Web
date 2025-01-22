from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from Models.user import UserCreate, User
from database import get_db
from repositories.user_repository import UserRepository
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# JWT settings
SECRET_KEY = "your-secret-key"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=["auth"])

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Connection = Depends(get_db)):
    existing_user = await UserRepository.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await UserRepository.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Could not create user")
    return new_user

@router.post("/login")
async def login(email: str, password: str, db: Connection = Depends(get_db)):
    user = await UserRepository.verify_password(db, email, password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    } 