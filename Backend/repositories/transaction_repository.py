from typing import Optional, List
from sqlite3 import Connection
from Models.transaction import TransactionCreate, Transaction

class TransactionRepository:
    @staticmethod
    async def create_transaction(conn: Connection, transaction: TransactionCreate) -> Optional[Transaction]:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO transactions 
                (wallet_id, from_wallet, recipient, status, transaction_type, 
                amount, created_at, tx_hash) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction.wallet_id,
                    transaction.from_wallet,
                    transaction.recipient,
                    transaction.status,
                    transaction.transaction_type,
                    transaction.amount,
                    transaction.created_at,
                    transaction.tx_hash
                )
            )
            conn.commit()
            return await TransactionRepository.get_transaction_by_id(conn, cursor.lastrowid)
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None

    @staticmethod
    async def get_transaction_by_id(conn: Connection, transaction_id: int) -> Optional[Transaction]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction_data = cursor.fetchone()
        
        if transaction_data:
            return Transaction(
                id=transaction_data[0],
                wallet_id=transaction_data[1],
                from_wallet=transaction_data[2],
                recipient=transaction_data[3],
                status=transaction_data[4],
                transaction_type=transaction_data[5],
                amount=transaction_data[6],
                created_at=transaction_data[7],
                tx_hash=transaction_data[8]
            )
        return None

    @staticmethod
    async def get_wallet_transactions(conn: Connection, wallet_id: int) -> List[Transaction]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM transactions WHERE wallet_id = ? ORDER BY created_at DESC", 
            (wallet_id,)
        )
        transactions = cursor.fetchall()
        
        return [
            Transaction(
                id=t[0],
                wallet_id=t[1],
                from_wallet=t[2],
                recipient=t[3],
                status=t[4],
                transaction_type=t[5],
                amount=t[6],
                created_at=t[7],
                tx_hash=t[8]
            )
            for t in transactions
        ]