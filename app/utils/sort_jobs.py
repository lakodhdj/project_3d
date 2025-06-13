from typing import List
from app.schemas.job import JobOut
from app.schemas.user import UserOut
from datetime import datetime

role_priority = {
    "глава лаборатории": 0,
    "преподаватель": 1,
    "студент": 2
}

def sort_jobs(jobs: List[JobOut], users: dict):
    """
    Сортирует заявки по приоритету роли и времени создания.
    Если дедлайн нужен, можно раскомментировать строку с deadline.
    users: словарь с ID пользователя и его ролью, например {1: "глава лаборатории", 2: "студент"}
    """
    return sorted(jobs, key=lambda x: (
        role_priority[users.get(x.user_id, "студент")],  # Приоритет роли
        x.deadline if x.deadline else datetime.max,   # Дедлайн (раскомментировать, если нужен)
        x.created_at                                     # Время создания
    ))