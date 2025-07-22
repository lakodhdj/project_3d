from sqlalchemy import Column, Integer, ForeignKey, Float, Date
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    printer_id = Column(Integer, ForeignKey("printers.id"), nullable=False)
    duration = Column(Float, nullable=False)  # Примерное время выполнения в часах
    deadline = Column(Date, nullable=True)  # Дедлайн в формате DD.MM.YYYY
    created_at = Column(Date, nullable=False)  # Скрытое поле даты добавления
    material_amount = Column(Float, nullable=False)  # Количество материала в граммах
    lead_time = Column(Integer, nullable=False) # Время выполнения в часах, округленное до большого
    priority = Column(Integer, nullable=False) # 1 = глава лаборатории, 2 = учитель, 3 S= студент
    

    # Установка связи с моделью User
    user = relationship("User", back_populates="jobs")
    # Установка связи с моделью Printer
    printer = relationship("Printer", back_populates="jobs")