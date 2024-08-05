import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Получаем URL базы данных из переменной окружения DATABASE_URL,
# если переменная не установлена, используется значение по умолчанию
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db/gym_project")

# Создание движка SQLAlchemy для подключения к базе данных PostgreSQL
# Мы устанавливаем некоторые параметры для управления пулом соединений:
# pool_size - максимальное количество соединений, поддерживаемых в пуле
# max_overflow - количество соединений, которые могут быть созданы сверх максимального размера пула
# pool_timeout - максимальное время ожидания (в секундах) перед выбросом исключения, если все соединения заняты
# pool_recycle - время (в секундах), через которое соединение будет перезапущено, чтобы избежать проблем с "зависшими" соединениями
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

# Создание фабрики сессий для управления соединениями с базой данных
# Сессия предоставляет основной интерфейс для работы с базой данных (запросы, транзакции и т.д.)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей SQLAlchemy
# Все классы моделей будут наследоваться от этого класса
Base = declarative_base()


# Функция-зависимость для получения экземпляра сессии базы данных
# Используется в FastAPI для инъекции зависимостей в обработчики запросов
def get_db():
    db = SessionLocal()  # Создаем экземпляр сессии
    try:
        yield db  # Возвращаем сессию для использования
    finally:
        db.close()  # Закрываем сессию после завершения работы
