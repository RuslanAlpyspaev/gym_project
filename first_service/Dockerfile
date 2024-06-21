# Используем базовый образ python:3.9-slim
FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в рабочую директорию
COPY . /app/

# Определяем команду по умолчанию
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "first_service.wsgi:application"]
