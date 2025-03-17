import os
from dotenv import load_dotenv

# Токен Telegram-бота
load_dotenv()
tokenTG = os.getenv('TOKEN')

if not tokenTG:
    raise ValueError("Ошибка: TOKEN не найден! Проверь файл .env")

