from pydantic import BaseModel, validator
from typing import Any, Dict
import json


# Базовая модель для описания среды
class EnvironmentBase(BaseModel):
    name: str  # Имя среды
    config: str  # Конфигурация среды в виде строки

    # Валидатор для проверки, что конфигурация является валидным JSON
    @validator("config")
    def validate_config(cls, value):
        try:
            # Попытка парсинга строки в JSON для проверки валидности
            json.loads(value)
        except json.JSONDecodeError:
            # Если произошла ошибка при парсинге, выбрасывается исключение
            raise ValueError("Config must be a valid JSON string")
        return value  # Возвращаем значение, если оно корректное


# Модель для создания новой среды
class EnvironmentCreate(EnvironmentBase):
    pass  # Используется, чтобы расширить базовую модель без изменений


# Модель для представления среды, как она будет храниться в базе данных
class Environment(EnvironmentBase):
    id: int  # Идентификатор среды (первичный ключ)
    owner_id: int  # Идентификатор владельца среды

    class Config:
        orm_mode = True  # Включаем режим ORM, чтобы работать с объектами ORM напрямую
