from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base
from sqlalchemy.orm import relationship

class Printer(Base):
    __tablename__ = "printers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Обратная связь с Job
    jobs = relationship("Job", back_populates="printer")