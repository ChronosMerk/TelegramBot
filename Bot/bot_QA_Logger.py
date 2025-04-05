import logging
import os
from datetime import datetime
from Bot.config import config
from Bot.log_to_telegram import TelegramLogHandler

# Генерируем уникальное имя файла логов с увеличением цифр
def get_log_filename():
    base_name = datetime.now().strftime('bat_log_%Y-%m-%d')
    counter = 1
    log_filename = os.path.join(config.log_dir, f"{base_name}_{counter}.log")

    # Проверка существования файла, если есть — увеличиваем цифру
    while os.path.exists(log_filename):
        counter += 1
        log_filename = os.path.join(config.log_dir, f"{base_name}_{counter}.log")
    return  log_filename

# Настройки логирования
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO,
    filename = get_log_filename(),
    filemode = 'w'
)

def starting_bot(name):
    logging.getLogger(name).info("Все завилось, Проверяй")
    print('Бот запущен')

"""Логирует вызов команды и ответ бота"""
def log_command(user, reply_message):
    if user.message:
        logging.getLogger(__name__).info('Пользователь %s (%s) вызвал %s', user.message.from_user.username,
                                         user.message.from_user.id, user.message.text)
        logging.getLogger(__name__).info('Отправлено сообщение пользователю %s (%s): "%s"', user.message.from_user.username,
                                         user.message.from_user.id, reply_message)
    elif user.callback_query:
        logging.getLogger(__name__).info('Пользователь %s (%s) вызвал %s', user.callback_query.from_user.username,
                                         user.callback_query.from_user.id, user.callback_query.data)
        logging.getLogger(__name__).info('Отправлено сообщение пользователю %s (%s): "%s"',
                                         user.callback_query.from_user.username, user.callback_query.from_user.id, reply_message)

def log_ai(name, user, prompt, reply):
    logging.getLogger(name).info(f"GPT-запрос от {user.username}: {prompt}")
    logging.getLogger(name).info(f"Ответ GPT: {reply}")