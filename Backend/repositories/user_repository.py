from typing import Optional, List
from sqlite3 import Connection
from Models.user import UserCreate, User
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    @staticmethod
    async def create_user(conn: Connection, user: UserCreate) -> Optional[User]:
        cursor = conn.cursor()
        try:
            hashed_password = pwd_context.hash(user.password)
            cursor.execute(
                "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                (user.email, hashed_password, datetime.utcnow())
            )
            conn.commit()
            return await UserRepository.get_user_by_email(conn, user.email)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    async def get_user_by_id(conn: Connection, user_id: int) -> Optional[User]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, created_at FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        if user_data:
            return User(
                id=user_data[0],
                email=user_data[1],
                created_at=user_data[2]
            )
        return None

    @staticmethod
    async def get_user_by_email(conn: Connection, email: str) -> Optional[User]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, created_at FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        
        if user_data:
            return User(
                id=user_data[0],
                email=user_data[1],
                created_at=user_data[2]
            )
        return None

    @staticmethod
    async def update_user(conn: Connection, user_id: int, email: str) -> Optional[User]:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET email = ? WHERE id = ?",
                (email, user_id)
            )
            conn.commit()
            return await UserRepository.get_user_by_id(conn, user_id)
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    @staticmethod
    async def delete_user(conn: Connection, user_id: int) -> bool:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    @staticmethod
    async def verify_password(conn: Connection, email: str, password: str) -> Optional[User]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password_hash, created_at FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        
        if user_data and pwd_context.verify(password, user_data[2]):
            return User(
                id=user_data[0],
                email=user_data[1],
                created_at=user_data[3]
            )
        return None 