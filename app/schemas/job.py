from pydantic import BaseModel
from datetime import datetime

class JobBase(BaseModel):
    user_id: int
    printer_id: int
    duration: float  # Время выполнения в часах (или минутах, в зависимости от вашей логики)
    deadline: datetime 

class JobCreate(JobBase):
    pass

class JobOut(JobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
