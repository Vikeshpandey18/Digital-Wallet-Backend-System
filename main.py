from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from . import models, schemas, auth
from .wallet import router as wallet_router

# 1️⃣ Create FastAPI app FIRST
app = FastAPI(title="Digital Wallet Backend")

# 2️⃣ Create database tables
models.Base.metadata.create_all(bind=engine)

# 3️⃣ Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4️⃣ REGISTER USER API
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_password = auth.hash_password(user.password)

    # create user
    new_user = models.User(
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # create wallet for user
    wallet = models.Wallet(owner=new_user)
    db.add(wallet)
    db.commit()

    return new_user

# 5️⃣ Include wallet routes
app.include_router(wallet_router)

@app.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        return {"error": "Invalid email or password"}

    if not auth.verify_password(user.password, db_user.password):
        return {"error": "Invalid email or password"}

    token = auth.create_access_token({"user_id": db_user.id})

    return {"access_token": token}

