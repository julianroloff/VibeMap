from fastapi import APIRouter, Depends, HTTPException
from models import User
from schemas import UserCreate, UserLogin, TokenResponse
from dependencies import create_access_token, verify_password, get_db
from sqlalchemy.orm import Session


router = APIRouter()

# Register User
@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, details = "Email already registered")
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}


# Login User
@router.post("/login", response_model = TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user.email})
    return {"access token": token, "token_type": "bearer"}