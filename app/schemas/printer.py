from pydantic import BaseModel

class PrinterBase(BaseModel):
    name: str

class PrinterCreate(PrinterBase):
    pass

class PrinterOut(PrinterBase):
    id: int

    class Config:
        from_attributes = True