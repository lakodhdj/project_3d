from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.user import User, UserRole
from schemas.user import UserCreate, UserOut, LoginRequest
from passlib.context import CryptContext
from jwt import encode
from datetime import datetime, timedelta
from typing import Annotated
from dependencies import SECRET_KEY, ALGORITHM, get_current_user, redis_client

router = APIRouter(prefix="/users/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

@router.post("/register", response_model=UserOut)
async def register_user(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserOut:
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует!")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hash_pass=hashed_password, role=user.role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login")
async def login(
    form_data: Annotated[LoginRequest, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response
) -> dict:
    user = await get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hash_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный пользователь или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    session_payload = {"sub": user.username, "user_id": user.id, "role": user.role.value, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    session_id = encode(session_payload, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=1800) 
    await redis_client.setex(f"session:{session_id}", 1800, str(user.id))  
    return {"message": "Успешно авторизованы!"}