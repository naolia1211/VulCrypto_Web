from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from Models.user import UserCreate, User
from database import get_db
from repositories.user_repository import UserRepository
from typing import List

router = APIRouter(tags=["users"])

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Connection = Depends(get_db)):
    existing_user = await UserRepository.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await UserRepository.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Could not create user")
    return new_user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Connection = Depends(get_db)):
    user = await UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, email: str, db: Connection = Depends(get_db)):
    user = await UserRepository.update_user(db, user_id, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Connection = Depends(get_db)):
    success = await UserRepository.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.post("/login")
async def login(email: str, password: str, db: Connection = Depends(get_db)):
    user = await UserRepository.verify_password(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
