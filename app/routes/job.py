from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobOut
from app.dependencies import get_current_user
from app.utils.sort_jobs import sort_jobs
from typing import List, Annotated

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobOut)
async def create_job(
    job: JobCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> JobOut:
    created_at = job.created_at.replace(tzinfo=None) if job.created_at.tzinfo else job.created_at
    deadline = job.deadline.replace(tzinfo=None) if job.deadline and job.deadline.tzinfo else job.deadline

    db_job = Job(
        printer_id=job.printer_id,
        duration=job.duration,
        created_at=created_at,
        deadline=deadline
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
        select(Job, User).join(User).where(Job.printer_id == printer_id, Job.status == "pending")
    )
    jobs = result.all()
    users = {job.User.id: job.User.role.value for job in jobs}
    sorted_jobs = sort_jobs([job.Job for job in jobs], users)
    return sorted_jobs