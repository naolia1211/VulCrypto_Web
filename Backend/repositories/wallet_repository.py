from typing import Optional
from sqlite3 import Connection
from Models.wallet import WalletCreate, Wallet
from decimal import Decimal
from datetime import datetime

class WalletRepository:
    @staticmethod
    async def create_wallet(conn: Connection, wallet: WalletCreate) -> Optional[Wallet]:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO wallets (address, balance, private_key, user_id) 
                VALUES (?, ?, ?, ?)
                """,
                (wallet.address, wallet.balance, wallet.private_key, wallet.user_id)
            )
            conn.commit()
            return await WalletRepository.get_wallet_by_user_id(conn, wallet.user_id)
        except Exception as e:
            print(f"Error creating wallet: {e}")
            return None

    @staticmethod
    async def get_wallet_by_user_id(conn: Connection, user_id: int) -> Optional[Wallet]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wallets WHERE user_id = ?", (user_id,))
        wallet_data = cursor.fetchone()
        
        if wallet_data:
            return Wallet(
                id=wallet_data[0],
                address=wallet_data[1],
                balance=Decimal(wallet_data[2]),
                private_key=wallet_data[3],
                user_id=wallet_data[4],
                created_at=wallet_data[5]
            )
        return None

    @staticmethod
    async def get_wallet_by_address(conn: Connection, address: str) -> Optional[Wallet]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wallets WHERE address = ?", (address,))
        wallet_data = cursor.fetchone()
        
        if wallet_data:
            return Wallet(
                id=wallet_data[0],
                address=wallet_data[1],
                balance=Decimal(wallet_data[2]),
                private_key=wallet_data[3],
                user_id=wallet_data[4],
                created_at=wallet_data[5]
            )
        return None 