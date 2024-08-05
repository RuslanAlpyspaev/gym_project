FROM python:3.9-slim

# Устанавливаем необходимые системные зависимости и инструменты для сборки
# Устанавливаем основные инструменты для сборки
# Устанавливаем библиотеку для работы с PostgreSQL
# Очищаем кэш apt-get для уменьшения размера образа
# Удаляем временные файлы apt для экономии места
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями Python в рабочую директорию
COPY requirements.txt .

# Обновляем pip до последней версии
RUN pip install --upgrade pip

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install -r requirements.txt

# Копируем содержимое локальной директории `app` в рабочую директорию контейнера
COPY ./app .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Команда для запуска FastAPI приложения с использованием Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
