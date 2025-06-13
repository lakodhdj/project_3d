# Импорт базового класса. Pydantic нужен для валидации данных и преобразования в Python-объекты
from pydantic import BaseModel
from app.models.user import UserRole


# Базовая схема
class UserBase(BaseModel):
    username: str
    role: UserRole

# Создание юзера. Наследует юзербейс и его поля
class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    
    # позволяет использовать Pydantic-схему с ORM
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str