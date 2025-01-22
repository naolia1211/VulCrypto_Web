import sqlite3
from contextlib import contextmanager

DATABASE_URL = "wallet.db"

async def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_URL)
    try:
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        if conn:
            conn.close()
        raise

async def init_db():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DATABASE_URL)
    try:
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT UNIQUE NOT NULL,
                balance DECIMAL(18,8) DEFAULT 0.0,
                private_key TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_id INTEGER NOT NULL,
                from_wallet TEXT NOT NULL,
                recipient TEXT NOT NULL,
                status TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount FLOAT NOT NULL,
                created_at INTEGER NOT NULL,
                tx_hash TEXT,
                FOREIGN KEY (wallet_id) REFERENCES wallets(id)
            );
            """
        ]
        
        for query in queries:
            conn.execute(query)
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise
    finally:
        conn.close()