from pydantic import BaseModel, Field
from datetime import date

class JobCreate(BaseModel):
    printer_id: int
    duration: int
    deadline: date  
    material_amount: int

    class Config:
        schema_extra = {
            "example": {
                "printer_id": 0,
                "duration": 0,
                "deadline": "2025-06-18T14:25:00",
                "material_amount": 0
            }
        }
        
class JobOut(JobCreate):
    id: int
    user_id: int
    created_at: date

    class Config:
        orm_mode = True