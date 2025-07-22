from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class JobCreate(BaseModel):
    printer_id: int
    duration: int
    deadline: date  # Pydantic преобразует строку в datetime
    material_amount: int
    lead_time: int

    class Config:
        schema_extra = {
            "example": {
                "printer_id": 1,
                "duration": 5,
                "deadline": "2025-06-18T14:25:00",
                "material_amount": 5,
                "lead_time": 0
            }
        }
        
class JobOut(JobCreate):
    id: int
    user_id: int
    created_at: date  # Скрытое поле, отображается в ответе

    class Config:
        orm_mode = True