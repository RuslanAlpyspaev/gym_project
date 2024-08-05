from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# Определяем класс User, представляющий пользователя в базе данных.
class User(Base):
    __tablename__ = "users"  # Имя таблицы в базе данных

    # Определяем столбцы таблицы
    id = Column(Integer, primary_key=True, index=True)  # Первичный ключ, автоинкрементируемый
    username = Column(String, unique=True, index=True)  # Имя пользователя, должно быть уникальным
    environments = relationship("Environment", back_populates="owner")  # Связь с таблицей Environment


# Определяем класс Environment, представляющий среду в базе данных.
class Environment(Base):
    __tablename__ = "environments"  # Имя таблицы в базе данных

    # Определяем столбцы таблицы
    id = Column(Integer, primary_key=True, index=True)  # Первичный ключ, автоинкрементируемый
    name = Column(String, index=True)  # Имя среды
    user_id = Column(Integer, ForeignKey("users.id"))  # Внешний ключ, ссылающийся на таблицу users
    config = Column(String)  # Конфигурация среды в виде строки

    owner = relationship("User", back_populates="environments")  # Связь с таблицей User
