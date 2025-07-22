from pydantic import BaseModel, Field

class MaterialCreate(BaseModel):
    name: str = Field(..., example="PLA")
    printer_id: int 
    quantity: float = Field(..., gt=0, example=5.0)  # Количество, больше 0

class MaterialOut(MaterialCreate):
    id: int

    class Config:
        orm_mode = True

class MaterialUpdate(BaseModel):
    quantity: float = Field(..., gt=0, example=10.0)
