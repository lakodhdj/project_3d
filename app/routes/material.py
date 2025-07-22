from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.material import Material  # Предполагаемая модель
from schemas.material import MaterialCreate, MaterialOut, MaterialUpdate  # Предполагаемые схемы
from typing import List, Annotated

router = APIRouter(prefix="/materials", tags=["materials"])

@router.post("/", response_model=MaterialOut)
async def add_material(
    material: MaterialCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> MaterialOut:
    db_material = Material(**material.dict())
    db.add(db_material)
    await db.commit()
    await db.refresh(db_material)
    return db_material


@router.get("/", response_model=List[MaterialOut])
async def list_materials(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> List[MaterialOut]:
    result = await db.execute(select(Material))
    materials = result.scalars().all()
    return materials

@router.patch("/{material_id}", response_model=MaterialOut)
async def update_material_quantity(material_id: int, data: MaterialUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Material).where(Material.id == material_id))
    material = result.scalar_one_or_none()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    material.quantity = data.quantity
    db.add(material)
    await db.commit()
    await db.refresh(material)
    return material
