from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from .database import SessionLocal
from .models import Wallet, Transaction
from .auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/wallet", tags=["Wallet"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---------------- CREDIT ----------------
@router.post("/add-money")
def add_money(
    amount: float,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    transaction = Transaction(
        amount=amount,
        type="credit",
        wallet=wallet
    )

    wallet.balance += amount
    db.add(transaction)
    db.commit()
    db.refresh(wallet)

    return {
        "message": "Money added successfully",
        "balance": wallet.balance
    }

# ---------------- DEBIT ----------------
@router.post("/pay")
def pay_money(
    amount: float,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # ❌ Prevent negative balance
    if wallet.balance < amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    transaction = Transaction(
        amount=amount,
        type="debit",
        wallet=wallet
    )

    wallet.balance -= amount
    db.add(transaction)
    db.commit()
    db.refresh(wallet)

    return {
        "message": "Payment successful",
        "balance": wallet.balance
    }
