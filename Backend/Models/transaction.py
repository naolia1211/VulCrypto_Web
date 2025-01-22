from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    wallet_id: int
    from_wallet: str
    recipient: str
    status: str
    transaction_type: str
    amount: float
    created_at: int
    tx_hash: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    
    class Config:
        from_attributes = True