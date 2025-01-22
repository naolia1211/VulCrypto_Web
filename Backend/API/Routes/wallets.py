from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from Models.wallet import WalletCreate, Wallet
from database import get_db
from repositories.wallet_repository import WalletRepository
from typing import List

router = APIRouter()

@router.post("/", response_model=Wallet)
async def create_wallet(wallet: WalletCreate, db: Connection = Depends(get_db)):
    new_wallet = await WalletRepository.create_wallet(db, wallet)
    if not new_wallet:
        raise HTTPException(status_code=400, detail="Could not create wallet")
    return new_wallet

@router.get("/{user_id}", response_model=Wallet)
async def get_wallet(user_id: int, db: Connection = Depends(get_db)):
    wallet = await WalletRepository.get_wallet_by_user_id(db, user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
