from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gym
import threading
import logging
from typing import Dict

# Создаем приложение FastAPI
app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Модель Pydantic для валидации данных запроса
class EnvironmentConfig(BaseModel):
    name: str
    episodes: int
    steps_per_episode: int


# Глобальные словари для отслеживания запущенных сред и управления потоками
running_environments: Dict[str, threading.Thread] = {}  # Хранит потоки запущенных сред
environment_locks: Dict[str, threading.Event] = {}  # Хранит события для управления остановкой потоков


@app.post("/run/")
def run_environment(config: EnvironmentConfig):
    """
    Запускает выполнение среды Gym в новом потоке.
    """
    # Проверка корректности имени среды
    valid_envs = [
        "CartPole-v1", "Acrobot-v1", "MountainCar-v0", "Pendulum-v1", "MountainCarContinuous-v0"
    ]
    if config.name not in valid_envs:
        raise HTTPException(status_code=400, detail="Invalid environment name")

    # Проверка, что среда не запущена
    if config.name in running_environments:
        raise HTTPException(status_code=400, detail=f"{config.name} is already running")

    # Создаем событие для управления остановкой потока
    stop_event = threading.Event()
    environment_locks[config.name] = stop_event

    # Запускаем новый поток для выполнения среды
    thread = threading.Thread(target=execute_environment, args=(config, stop_event))
    thread.start()

    # Сохраняем информацию о запущенной среде
    running_environments[config.name] = thread

    return {"detail": f"Started running {config.name}"}


def execute_environment(config: EnvironmentConfig, stop_event: threading.Event):
    """
    Выполняет среду Gym с заданной конфигурацией.
    """
    try:
        # Создаем среду
        env = gym.make(config.name)
        for episode in range(config.episodes):
            observation = env.reset()  # Сбрасываем среду
            for step in range(config.steps_per_episode):
                # Проверяем, было ли установлено событие остановки
                if stop_event.is_set():
                    logger.info(f"Execution of {config.name} has been stopped.")
                    return
                env.render()  # Отображаем текущую ситуацию в среде
                action = env.action_space.sample()  # Выбираем случайное действие
                observation, reward, done, _ = env.step(action)  # Выполняем действие
                if done:  # Если эпизод завершен, выходим из цикла
                    break
            logger.info(f"Completed episode {episode + 1} of {config.name}")
        env.close()  # Закрываем среду после выполнения всех эпизодов
    except Exception as e:
        logger.error(f"Error running {config.name}: {str(e)}")
    finally:
        # Удаляем среду из запущенных и освобождаем ресурсы
        if config.name in running_environments:
            del running_environments[config.name]
        if config.name in environment_locks:
            del environment_locks[config.name]


@app.post("/stop/{env_name}")
def stop_environment(env_name: str):
    """
    Останавливает выполнение запущенной среды.
    """
    # Проверяем, что среда действительно запущена
    if env_name not in running_environments:
        raise HTTPException(status_code=404, detail=f"{env_name} is not running")

    # Устанавливаем событие остановки
    stop_event = environment_locks.get(env_name)
    if stop_event:
        stop_event.set()

    # Ожидаем завершения потока
    thread = running_environments[env_name]
    thread.join()  # Это обеспечит безопасное завершение потока

    # Очищаем данные о запущенной среде
    del running_environments[env_name]
    if env_name in environment_locks:
        del environment_locks[env_name]

    return {"detail": f"Stopped running {env_name}"}
