# Используем официальный образ Python в качестве базового
FROM python:3.9-slim

# Устанавливаем Git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы и устанавливаем зависимости
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

# Запускаем тесты во время сборки
RUN python -m unittest discover -s tests

CMD ["python", "app.py"]
