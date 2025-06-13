from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from app.database import Base
from datetime import datetime
from app.models.user import User
from app.models.printer import Printer

# логическое связывание моделей на уровне питона
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    printer_id = Column(Integer, ForeignKey("printers.id"))
    duration = Column(Float)  
    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime, nullable=True)
    # установка связи между job и users. позволяет получить пользователя по заданию. back_populates="jobs" - поле в User, которое хранит все задания пользователя
    user = relationship("User", back_populates="jobs")
    printer = relationship("Printer", back_populates="jobs")

User.jobs = relationship("Job", order_by=Job.created_at, back_populates="user")
Printer.jobs = relationship("Job", order_by=Job.created_at, back_populates="printer")
