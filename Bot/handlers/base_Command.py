from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
from Bot.bot_QA_Logger import log_command, starting_bot
from Bot.config import config
from Bot.handlers.dowload_movies import download_video

class QABot:
    """Класс Telegram-бота для QA"""

    def __init__(self):
        """Инициализация бота"""
        self.application = ApplicationBuilder().token(config.tokenTG).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Регистрация команд"""
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^(https?://)?(www\.)?(instagram\.com|.*\.tiktok\.com)/'),download_video))

        # Неизвестные команды и текстовые сообщения (всегда последними!)
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_message))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.unknown_message))

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        user = update.message
        reply_message = f"Привет, {user.from_user.first_name}! Я Бот Hidden protocol для группы,Животные в своей среде обитания !"

        await update.message.reply_text(reply_message)
        log_command(update, reply_message)

    # Обработчик неизвестных команд и сообщений
    @staticmethod
    async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "/" in update.message.text and "https://" not in update.message.text:
            random_responses = [
                "⛔ Неизвестная команда. Хочешь разорвать петлю? Сначала узнай, как она устроена.",
                "🔍 Сигнал нераспознан. Попробуй /help — или продолжай искать в темноте.",
                "🕳 Ты активировал пустоту. Она молчит в ответ.",
                "⚠️ Протокол не обнаружен. Возможно, он ещё не создан."
            ]
            unknown_responses = f'⛔ Ошибка 404: Команда не распознана. \n{random.choice(random_responses)}'
            await update.message.reply_text(unknown_responses)
            log_command(update, random_responses)

    def run(self):
        """Запуск бота"""
        starting_bot()
        self.application.run_polling()
