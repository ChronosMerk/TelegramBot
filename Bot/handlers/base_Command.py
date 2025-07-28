from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
from Bot.bot_QA_Logger import log_command, starting_bot
from Bot.handlers.message_Handler import button_handler
from Bot.metrics import track_command, track_response_time
from Bot.config import config
from Ai.GPT import handle_gpt
from Bot.handlers.dowload_movies import download_video
from Bot.handlers.help_handlers import help_command

class QABot:
    """Класс Telegram-бота для QA"""

    def __init__(self):
        """Инициализация бота"""
        self.application = ApplicationBuilder().token(config.tokenTG).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Регистрация команд"""
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('help', help_command))
        self.application.add_handler(CommandHandler('categories', self.categories))
        #self.application.add_handler(CommandHandler('deepseek ', self.deepseek))
        self.application.add_handler(CommandHandler('gpt', handle_gpt))
        self.application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^(https?://)?(www\.)?(instagram\.com|tiktok\.com|vt\.tiktok\.com)/'),download_video))

        # Обработчик нажатий на кнопки
        self.application.add_handler(CallbackQueryHandler(button_handler))

        # Неизвестные команды и текстовые сообщения (всегда последними!)
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_message))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.unknown_message))

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        with track_response_time(update.message.text):
            user = update.message
            reply_message = f"Привет, {user.from_user.first_name}! Я QA-бот, который поможет тебе изучить QA!"

            await update.message.reply_text(reply_message)
            log_command(update, reply_message)
            track_command(update.message.text)

    @staticmethod
    async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /categories"""
        with track_response_time(update.message.text):
            keyboard = [
                [InlineKeyboardButton("📌 Manual QA", callback_data="manual")],
                [InlineKeyboardButton("🤖 Automation QA", callback_data="automation")],
                [InlineKeyboardButton("🛠 Инструменты", callback_data="tools")],
                [InlineKeyboardButton("📚 Методологии", callback_data="methodologies")],
                [InlineKeyboardButton("❓ QAQ", callback_data="qaq")],
                [InlineKeyboardButton("✅ Чек-листы", callback_data="checklists")],
                [InlineKeyboardButton("🔒 Security Testing", callback_data="security")],
            ]

            reply_message = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text("📂 Доступные категории статей:", reply_markup=reply_message)
            log_command(update, reply_message)
            track_command(update.message.text)

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
            track_command("unknown")

    def run(self):
        """Запуск бота"""
        starting_bot()
        self.application.run_polling()
