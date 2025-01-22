from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from database import init_db, get_db
from contextlib import asynccontextmanager
import sqlite3
from passlib.context import CryptContext
from API import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Define allowed origins
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    # Add any other origins you need
]

# Add CORS middleware before including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include router after CORS middleware
app.include_router(router)

@app.options("/{full_path:path}")
async def options_handler():
    return {"detail": "OK"}

if __name__ == "__main__":
    import uvicorn
    print(f"CORS Origins configured: {origins}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    