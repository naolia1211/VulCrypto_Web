from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class WalletBase(BaseModel):
    address: str
    balance: Decimal = Decimal('0.00')
    private_key: str
    user_id: int

class WalletCreate(WalletBase):
    pass

class Wallet(WalletBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
