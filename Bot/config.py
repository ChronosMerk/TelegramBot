import os
from dotenv import load_dotenv

# Токен Telegram-бота
load_dotenv()
tokenTG = os.getenv('TOKEN')
tokenDeepSeek = os.getenv('TOKENDEEPSEEK')

if not tokenTG:
    raise ValueError("Ошибка: TOKEN не найден! Проверь файл .env")

LOG_DIR = r'G:\Docker\Log'

# Создать папку для логов, если её нет
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

prometheus_port = 8000