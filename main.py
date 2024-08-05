# Рабочий майн в первом сервисе, этот нужен для того чтобы докер запустился в IDE
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String  # Импорт модулей для работы с базой данных
from sqlalchemy.ext.declarative import declarative_base  # Импорт для создания базового класса моделей
from sqlalchemy.orm import sessionmaker, Session  # Импорт модулей для работы с сессиями базы данных
from pydantic import BaseModel  # Импорт базовой модели Pydantic
import requests
import os
from loguru import logger  # Импорт Loguru для логирования
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Импорт для работы с OAuth2

# Настройка базы данных
# Используем переменные окружения для получения URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/gym_project")

# Создаем движок SQLAlchemy для подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий для управления подключениями к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Инициализация приложения FastAPI
app = FastAPI()

# Определение схемы OAuth2 с использованием password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Псевдо-хранилище пользователей (в реальном проекте применил бы дополнительную БД)
fake_users_db = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$KIXHtD4xJcQ8q5RVJd9xhuo2BKEF6F61gjvUIR9W9sM0kY1JBOzqG",  # "secret"
        "disabled": False,
    },
}


# Функция для верификации пароля
def verify_password(plain_password, hashed_password):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


# Функция для аутентификации пользователя
def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


# Эндпоинт для получения токена
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Эндпоинт для входа и получения токена доступа.
    :param form_data: Данные формы для входа (username и password).
    :return: Токен доступа.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # В реальном проекте здесь нужно создавать и возвращать JWT-токен
    return {"access_token": user["username"], "token_type": "bearer"}


# Функция для получения текущего пользователя по токену
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_users_db.get(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# Определение модели базы данных для хранения данных о средах Gym
class GymEnvironment(Base):
    __tablename__ = "environments"  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор
    name = Column(String, index=True)  # Название среды
    episodes = Column(Integer)  # Количество эпизодов
    steps_per_episode = Column(Integer)  # Количество шагов в каждом эпизоде


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


# Определение модели Pydantic для валидации входных данных API
class EnvironmentCreate(BaseModel):
    name: str  # Название среды
    episodes: int  # Количество эпизодов
    steps_per_episode: int  # Количество шагов в эпизоде


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Эндпоинт для создания новой среды Gym
@app.post("/environments/")
async def create_environment(
        env: EnvironmentCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Только авторизованные пользователи могут создавать среды
):
    """
    Создание новой среды в базе данных.
    :param env: Данные конфигурации среды.
    :param db: Сессия базы данных.
    :param current_user: Текущий авторизованный пользователь.
    :return: Созданная среда.
    """
    # Валидация названия среды
    valid_envs = [
        "CartPole-v1", "Acrobot-v1", "MountainCar-v0", "Pendulum-v1", "MountainCarContinuous-v0"
    ]
    if env.name not in valid_envs:
        logger.error(f"Неверное название среды: {env.name}")
        raise HTTPException(status_code=400, detail="Invalid environment name")

    # Создание новой записи в базе данных
    db_env = GymEnvironment(**env.dict())
    db.add(db_env)
    db.commit()
    db.refresh(db_env)
    logger.info(f"Создана среда: {db_env}")
    return db_env


# Эндпоинт для получения информации о среде по ID
@app.get("/environments/{env_id}")
async def read_environment(
        env_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Только авторизованные пользователи могут получать среды
):
    """
    Получение данных о среде из базы данных по ID.
    :param env_id: ID среды.
    :param db: Сессия базы данных.
    :param current_user: Текущий авторизованный пользователь.
    :return: Найденная среда.
    """
    db_env = db.query(GymEnvironment).filter(GymEnvironment.id == env_id).first()
    if db_env is None:
        logger.error(f"Среда не найдена: {env_id}")
        raise HTTPException(status_code=404, detail="Environment not found")
    return db_env


# Эндпоинт для удаления среды по ID
@app.delete("/environments/{env_id}")
async def delete_environment(
        env_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Только авторизованные пользователи могут удалять среды
):
    """
    Удаление среды из базы данных по ID.
    :param env_id: ID среды.
    :param db: Сессия базы данных.
    :param current_user: Текущий авторизованный пользователь.
    :return: Сообщение о выполнении операции.
    """
    db_env = db.query(GymEnvironment).filter(GymEnvironment.id == env_id).first()
    if db_env is None:
        logger.error(f"Среда не найдена: {env_id}")
        raise HTTPException(status_code=404, detail="Environment not found")
    db.delete(db_env)
    db.commit()
    logger.info(f"Удалена среда: {env_id}")
    return {"detail": "Environment deleted"}


# Эндпоинт для запуска среды по ID
@app.post("/run/{env_id}")
async def run_environment(
        env_id: int,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Только авторизованные пользователи могут запускать среды
):
    """
    Запуск среды на втором сервисе по ID.
    :param env_id: ID среды.
    :param db: Сессия базы данных.
    :param current_user: Текущий авторизованный пользователь.
    :return: Сообщение о выполнении операции.
    """
    db_env = db.query(GymEnvironment).filter(GymEnvironment.id == env_id).first()
    if db_env is None:
        logger.error(f"Среда не найдена: {env_id}")
        raise HTTPException(status_code=404, detail="Environment not found")

    # Преобразование объекта SQLAlchemy в словарь
    db_env_dict = {
        "name": db_env.name,
        "episodes": db_env.episodes,
        "steps_per_episode": db_env.steps_per_episode
    }

    # Отправка конфигурации на второй сервис
    try:
        response = requests.post("http://second_service:8001/run/", json=db_env_dict)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Не удалось запустить среду {env_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to start environment execution")

    logger.info(f"Запущено выполнение среды для {env_id}")
    return {"detail": "Environment execution started", "response": response.json()}
