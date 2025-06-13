# импорта класса CryptContext для настройки и использования алгоритмов хэширования (bcrypt)
from passlib.context import CryptContext

# Импорт HTTPException - генерация HTTP ошибок и статус ответа
from fastapi import HTTPException, status

# указание алгоритма bcrypt
context = CryptContext(schemes=["bcrypt"])

# функция хэширования пароля
def hashed_password(password: str) -> str:
    return context.hash(password)

 # функция проверки введенного пароля с паролем при регистрации в бд хэшированный
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)