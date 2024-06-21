Gym Project
Описание
Этот проект состоит из двух сервисов, которые работают вместе для настройки и запуска различных сред OpenAI Gym. Первый сервис отвечает за конфигурацию среды и сохранение её в базе данных, второй сервис отвечает за запуск среды и стриминг её выполнения. Проект использует Django для веб-фреймворка, Celery для задач асинхронного выполнения и Docker для контейнеризации.


Запуск проекта
Предварительные требования
Docker
Docker Compose
Установка и запуск
Клонируйте репозиторий на ваш локальный компьютер:
bash

git clone 
cd gym_project
Создайте и запустите контейнеры Docker:
bash

docker-compose up --build
Выполните миграции для базы данных:
bash

docker-compose run first_service python manage.py migrate
Создайте суперпользователя для доступа к административной панели Django:
bash

docker-compose run first_service python manage.py createsuperuser
Перезапустите контейнеры для применения изменений:
bash

docker-compose down
docker-compose up
Теперь вы можете получить доступ к административной панели Django по адресу http://localhost:8000/admin и настроить ваши среды Gym.

Конфигурация
Первый сервис (first_service)
Первый сервис отвечает за конфигурирование среды и сохранение её в базе данных. Он предоставляет API для взаимодействия с пользователями и средами.

Второй сервис (second_service)
Второй сервис отвечает за запуск сред и обработку задач с использованием Celery. Он запускает среды в соответствии с конфигурацией, переданной от первого сервиса.

Endpoints
Первый сервис (first_service)
GET /api/users/ - Получить список пользователей
POST /api/users/ - Создать нового пользователя
GET /api/environments/ - Получить список сред
POST /api/environments/ - Создать новую среду
Второй сервис (second_service)
POST /api/start_acrobot/ - Запустить среду Acrobot
POST /api/start_cartpole/ - Запустить среду CartPole
POST /api/start_mountaincar/ - Запустить среду MountainCar
POST /api/start_mountaincar_continuous/ - Запустить среду MountainCarContinuous
POST /api/start_pendulum/ - Запустить среду Pendulum

Использование

Сначала создайте пользователя и среду через API первого сервиса или через административную панель Django.
Отправьте запрос на запуск среды через API второго сервиса.
