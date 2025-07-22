from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base
from sqlalchemy.orm import relationship

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    printer_id = Column(Integer, ForeignKey("printers.id"), nullable=False)
    quantity = Column(Float, nullable=False)

    printer = relationship("Printer", back_populates="materials")