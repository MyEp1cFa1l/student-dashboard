FROM python:3.13-slim

# Не создавать .pyc файлы и выводить логи без задержек
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем системные зависимости (нужны для компиляции psycopg2)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]