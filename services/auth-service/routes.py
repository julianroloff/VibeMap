from fastapi import APIRouter, Depends, HTTPException
from models import User
from schemas import UserCreate, UserLogin, TokenResponse
from dependencies import create_access_token, verify_password, get_db, get_current_user, pwd_context
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

# Register User
@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password before storing
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "user_id": new_user.id})
    return {"access_token": token, "token_type": "bearer"}


# Login User (Fixed: Uses AsyncSession)
@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email, "user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"} 


# Get User Info (Ensures Authenticated Requests)
@router.get("/me")
async def get_user_info(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email, "id": current_user.id, "profilePicture": current_user.profile_picture}
