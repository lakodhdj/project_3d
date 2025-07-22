from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.job import Job
from models.user import User
from schemas.job import JobCreate, JobOut
from dependencies import get_current_user
from typing import List, Annotated
from datetime import date, datetime, timedelta, timezone

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobOut)
async def create_job(job: JobCreate, 
                     db: Annotated[AsyncSession, Depends(get_db)], 
                     current_user: Annotated[User, Depends(get_current_user)]) -> JobOut:
    priority_dct = {"глава лаборатории": 1, "учитель": 2, "студент": 3}
    priority = priority_dct.get(current_user.role, 3)

    from datetime import datetime

    deadline = job.deadline

    if deadline < datetime.now(timezone.utc).date():
        raise HTTPException(status_code=400, detail="Дедлайн не может быть в прошлом")

    
    # start_of_day = deadline.replace(hour=0, minute=0, second=0, microsecond=0)
    # end_of_day = start_of_day.replace(hour=23, minute=59, second=59)
    # result = await db.execute(
    #     select(sum(Job.duration)).where(Job.printer_id == job.printer_id).where(Job.deadline.between(start_of_day, end_of_day))
    # )

    # total_duration = result.scalar_one or 0

    # if total_duration + job.duration > 24:
    #     raise HTTPException(status_code=400, detail="Суммарное время заявок в этот день превышает 24 часа")
    
    # if job.duration > 8:
    #     deadline = deadline.replace(hour=20, minute=0)  
    #     if deadline.date() < datetime.now(timezone.utc).date():
    #         deadline = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=20, minute=0)

    db_job = Job(
        user_id = current_user.id,
        printer_id = job.printer_id,
        duration=job.duration,
        deadline=deadline,
        created_at=datetime.utcnow(),
        material_amount=job.material_amount,
        lead_time = job.lead_time ,
        priority=priority
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