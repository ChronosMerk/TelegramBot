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

logger = logging.getLogger(__name__)

def log_command(user, reply_message):
    """Логирует вызов команды и ответ бота"""
    logger.info('Пользователь %s (%s) вызвал %s', user.from_user.username, user.from_user.id, user.text)
    logger.info('Отправлено сообщение пользователю %s (%s): "%s"', user.from_user.username, user.from_user.id, reply_message)