from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class JobCreate(BaseModel):
    printer_id: int = Field(..., description="ID of the printer, selected from a dropdown on the frontend")
    duration: float = Field(..., description="Estimated duration in hours, chosen by user")
    deadline: date = Field(..., description="Deadline date in DD.MM.YYYY format, selected via calendar")
    material_amount: float = Field(..., description="Amount of material in units, chosen by user")

class JobOut(JobCreate):
    id: int
    user_id: int
    created_at: date  # Скрытое поле, отображается в ответе

    class Config:
        orm_mode = True