from telegram import Update
from telegram.ext import ContextTypes
from Bot.bot_QA_Logger import log_command
from Bot.metrics import track_command

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MESSAGE_HELP = '''🧭 Команды Скрытого Протокола:

/scan — анализ и сбор входящих данных
/decrypt — попытка расшифровки найденного артефакта
/path — прогноз возможных путей развития событий
/profile — досье на тебя
/update — внесение события в хронику
/echo — извлечение послания из временного вихря

⚠️ Внимание: доступ к командам может расширяться с ростом доверия Протокола.'''
    await update.message.reply_text(MESSAGE_HELP)
    log_command(update, MESSAGE_HELP)
    track_command(update.message.text)