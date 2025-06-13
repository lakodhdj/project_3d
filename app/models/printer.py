from sqlalchemy import Column, Integer, String
from app.database import Base

class Printer(Base):
    __tablename__ = "printers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)