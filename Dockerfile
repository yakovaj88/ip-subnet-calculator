# Dockerfile.test

# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (если необходимо)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app/

# Запускаем тесты во время сборки
RUN python -m unittest discover -s tests

# Удаляем ненужные зависимости после тестирования (опционально)
RUN apt-get purge -y build-essential && apt-get autoremove -y

# Нет команды CMD, так как этот Dockerfile предназначен только для тестирования
