from fastapi import APIRouter
from API.Routes import transactions, users, wallets, auth
from fastapi.responses import JSONResponse

router = APIRouter()

router.include_router(auth.router, prefix="/api/auth", tags=["auth"])
router.include_router(users.router, prefix="/api/users", tags=["users"])
router.include_router(wallets.router, prefix="/api/wallets", tags=["wallets"])
router.include_router(
    transactions.router, prefix="/api/transactions", tags=["transactions"]
)


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Crypto Wallet API"})
