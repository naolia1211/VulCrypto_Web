from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from Models.transaction import TransactionCreate, Transaction
from database import get_db
from repositories.transaction_repository import TransactionRepository
from typing import List

router = APIRouter()

@router.post("/", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, db: Connection = Depends(get_db)):
    new_transaction = await TransactionRepository.create_transaction(db, transaction)
    if not new_transaction:
        raise HTTPException(status_code=400, detail="Could not create transaction")
    return new_transaction

@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int, db: Connection = Depends(get_db)):
    transaction = await TransactionRepository.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/wallet/{wallet_id}", response_model=List[Transaction])
async def get_wallet_transactions(wallet_id: int, db: Connection = Depends(get_db)):
    transactions = await TransactionRepository.get_wallet_transactions(db, wallet_id)
    return transactions
