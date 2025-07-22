from pydantic import BaseModel

class PrinterBase(BaseModel):
    name: str

class PrinterCreate(PrinterBase):

    class Config:
        schema_extra = {
            "example": {
                "name": "printer_1"
            }
        }

class PrinterOut(PrinterBase):
    name: str
    id: int
    user_id: int
    username: str

    class Config:
        from_attributes = True