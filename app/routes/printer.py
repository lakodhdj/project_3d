from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.printer import Printer
from models.user import UserRole, User
from schemas.printer import PrinterCreate, PrinterOut
from dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/printers", tags=["printers"])

@router.post("/", response_model=PrinterOut)
async def create_printer(printer: PrinterCreate, current_user: Annotated[User, Depends(get_current_user)], db: AsyncSession = Depends(get_db), ) -> PrinterOut:
    if current_user.role != UserRole.lab_head:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only lab head can create printers"
        )
        
    existing = await db.execute(select(Printer).where(Printer.name == printer.name))
    if existing.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Printer with this name already exists"
        )
    db_printer = Printer(
        name=printer.name,
        user_id=current_user.id,  # Берем id напрямую из объекта User
        username=current_user.username  # Берется из текущего пользователя
    )
    db.add(db_printer)
    await db.commit()
    await db.refresh(db_printer)
    return db_printer

@router.get("/", response_model=List[PrinterOut])
async def get_printers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Printer))
    printers = result.scalars().all()
    return printers