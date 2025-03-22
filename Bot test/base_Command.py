from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from bot_QA_Logger import log_command, starting_bot
from message_Handler import button_handler
from config import tokenTG

class QABot:
    """Класс Telegram-бота для QA"""

    def __init__(self):
        """Инициализация бота"""
        self.application = ApplicationBuilder().token(tokenTG).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Регистрация команд"""
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('help', self.help))
        self.application.add_handler(CommandHandler('categories', self.categories))

        # Обработчик нажатий на кнопки
        self.application.add_handler(CallbackQueryHandler(button_handler))

        # Неизвестные команды и текстовые сообщения (всегда последними!)
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_message))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.unknown_message))

    # Обработчик неизвестных команд и сообщений
    @staticmethod
    async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_message = "Извини, я не понимаю эту команду."

        await update.message.reply_text(reply_message)
        log_command(update, reply_message)

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        user = update.message
        reply_message = f"Привет, {user.from_user.first_name}! Я QA-бот, который поможет тебе изучить QA!"

        await update.message.reply_text(reply_message)
        log_command(update, reply_message)

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help"""
        reply_message = "Основные команды бота: \n/start — приветствие и описание возможностей бота. \n/help — краткая инструкция по использованию и список доступных команд. \n/categories — отображение списка категорий (например, «Manual QA», «Automation QA», «Инструменты», «Методологии», «QAQ» и т.д.)."

        await update.message.reply_text(reply_message)
        log_command(update,reply_message)

    @staticmethod
    async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    def run(self):
        """Запуск бота"""
        starting_bot()
        self.application.run_polling()
