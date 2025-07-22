from fastapi import Depends, HTTPException, status, Request
from jwt import PyJWTError, decode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.user import User
from typing import Annotated
from dotenv import load_dotenv
import os
import redis.asyncio as redis
import asyncio

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

async def get_current_user(request: Request, db: Annotated[AsyncSession, Depends(get_db)]) -> User:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No session found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = decode(session_id, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        redis_key = f"session:{session_id}"
        cached_user_id = await redis_client.get(redis_key)
        if cached_user_id:
            result = await db.execute(select(User).where(User.id == int(cached_user_id.decode())))
            user = result.scalar_one_or_none()
            if user and user.username == username:
                return user

        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user:
            await redis_client.setex(redis_key, 1800, str(user.id))  # Кэшируем на 30 минут
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def close_redis():
    await redis_client.aclose()