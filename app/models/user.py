# Column - колонка в таблице и типы данных
from sqlalchemy import Column, Integer, String, Enum

# импорт базы моделей
from app.database import Base
import enum


class UserRole(enum.Enum):
    student = "студент"
    teacher = "учитель"
    lab_head = "глава лаборатории"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index = True)
    username = Column(String, unique = True, index = True)
    hash_pass = Column(String)
    role = Column(Enum(UserRole), default=UserRole.student)