from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.printer import Printer
from app.models.user import UserRole
from app.schemas.printer import PrinterCreate, PrinterOut
from app.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/printers", tags=["printers"])

@router.post("/", response_model=PrinterOut)
async def create_printer(printer: PrinterCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != UserRole.lab_head:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only lab head can create printers"
        )
    db_printer = Printer(name=printer.name)
    db.add(db_printer)
    await db.commit()
    await db.refresh(db_printer)
    return db_printer

@router.get("/", response_model=List[PrinterOut])
async def get_printers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Printer))
    printers = result.scalars().all()
    return printers