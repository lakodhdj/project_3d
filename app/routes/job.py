from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobOut
from app.dependencies import get_current_user
from typing import List, Annotated
from datetime import date

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobOut)
async def create_job(
    job: JobCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> JobOut:
    # Устанавливаем текущую дату как дату добавления
    created_at = date.today()
    # Создаем запись в базе
    db_job = Job(
        user_id=current_user.id,
        printer_id=job.printer_id,
        duration=job.duration,
        deadline=job.deadline,
        created_at=created_at,
        material_amount=job.material_amount
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

@router.get("/queue/{printer_id}", response_model=List[JobOut])
async def get_queue(
    printer_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> List[JobOut]:
    result = await db.execute(
        select(Job).where(Job.printer_id == printer_id)
    )
    jobs = result.scalars().all()
    return jobs