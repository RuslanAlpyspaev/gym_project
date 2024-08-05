import gym
import os
import json
from celery import Celery
from celery.utils.log import get_task_logger
from typing import Dict

# Настройка Celery с использованием брокера сообщений RabbitMQ
celery = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL', 'amqp://rabbitmq'))

# Настройка логгера для задач Celery
logger = get_task_logger(__name__)


@celery.task
def run_environment_task(name: str, config: str):
    """
    Запуск задачи Gym среды с заданной конфигурацией.

    :param name: Название среды Gym, которую нужно запустить.
    :param config: Строка конфигурации, закодированная в формате JSON.
    """
    try:
        # Разбор конфигурации из JSON-строки
        config_data = json.loads(config)
        episodes = config_data.get("episodes", 1)  # Получение количества эпизодов
        steps_per_episode = config_data.get("steps_per_episode", 1000)  # Получение количества шагов на эпизод

        # Создание среды Gym
        env = gym.make(name)

        # Выполнение среды
        for episode in range(episodes):
            observation = env.reset()  # Сбрасываем среду в начальное состояние
            for step in range(steps_per_episode):
                # Логирование текущего состояния для отладки или стриминга
                logger.debug(f"Episode {episode + 1}, Step {step + 1}: Observation: {observation}")

                # Случайное действие для демонстрации; можно заменить на действие AI-модели
                action = env.action_space.sample()

                # Выполнение действия
                observation, reward, done, _ = env.step(action)

                # Логирование результата действия
                logger.debug(f"Action: {action}, Reward: {reward}, Done: {done}")

                # Проверяем, завершена ли среда
                if done:
                    logger.info(f"Episode {episode + 1} ended after {step + 1} steps")
                    break

            # Логирование завершения каждого эпизода
            logger.info(f"Completed episode {episode + 1} of {name}")

        # Закрытие среды
        env.close()
        logger.info(f"Completed running environment {name}")

    # Обработка ошибок среды Gym
    except gym.error.Error as gym_error:
        logger.error(f"Gym error in environment {name}: {gym_error}")

    # Обработка ошибок при разборе JSON
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON config for environment {name}: {config}")

    # Обработка других неожиданных ошибок
    except Exception as e:
        logger.error(f"Unexpected error running environment {name}: {e}")
