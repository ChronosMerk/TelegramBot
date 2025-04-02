# --------------------------
# 📦 Dockerfile
# --------------------------
FROM python:3.11-slim

# Создаём рабочую директорию
WORKDIR /app

# Копируем весь проект
COPY .. .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Команда запуска
CMD ["python", "Bot/start_Bot.py"]
