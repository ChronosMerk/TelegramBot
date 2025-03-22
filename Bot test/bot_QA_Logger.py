import logging
import os
from datetime import datetime
from config import LOG_DIR

# Генерируем уникальное имя файла логов с увеличением цифр
def get_log_filename():
    base_name = datetime.now().strftime('bat_log_%Y-%m-%d')
    counter = 1
    log_filename = os.path.join(LOG_DIR, f"{base_name}_{counter}.log")

    # Проверка существования файла, если есть — увеличиваем цифру
    while os.path.exists(log_filename):
        counter += 1
        log_filename = os.path.join(LOG_DIR, f"{base_name}_{counter}.log")
    return  log_filename

# Настройки логирования
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO,
    filename = get_log_filename(),
    filemode = 'w'
)

def starting_bot():
    logging.getLogger(__name__).info("Все завилось, Проверяй")

"""Логирует вызов команды и ответ бота"""
def log_command(user, reply_message):
    logging.getLogger(__name__).info('Пользователь %s (%s) вызвал %s', user.from_user.username, user.from_user.id, user.text)
    logging.getLogger(__name__).info('Отправлено сообщение пользователю %s (%s): "%s"', user.from_user.username, user.from_user.id, reply_message)
