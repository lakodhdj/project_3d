from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base
from sqlalchemy.orm import relationship

class Printer(Base):
    __tablename__ = "printers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    username = Column(String, nullable=False)


    # Обратная связь с Job
    jobs = relationship("Job", back_populates="printer")
    materials = relationship('Material', back_populates='printer')