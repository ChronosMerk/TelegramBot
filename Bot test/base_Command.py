from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bot_QA_Logger import logger, log_command
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

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        user = update.message
        reply_message = f"Привет, {user.from_user.first_name}! Я QA-бот, который поможет тебе изучить QA!"

        await update.message.reply_text(reply_message)
        log_command(user,reply_message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help"""
        user = update.message
        reply_message = "Основные команды бота: \n/start — приветствие и описание возможностей бота. \n/help — краткая инструкция по использованию и список доступных команд. \n/categories — отображение списка категорий (например, «Manual QA», «Automation QA», «Инструменты», «Методологии», «QAQ» и т.д.)."

        await update.message.reply_text(reply_message)
        log_command(user,reply_message)

    def run(self):
        """Запуск бота"""
        logger.info("Все завилось, Проверяй")
        self.application.run_polling()

'''async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    keyboard = [
        [InlineKeyboardButton("📌 Manual QA", callback_data="manual")],
        [InlineKeyboardButton("🤖 Automation QA", callback_data="automation")],
        [InlineKeyboardButton("🛠 Инструменты", callback_data="tools")],
        [InlineKeyboardButton("📚 Методологии", callback_data="methodologies")],
        [InlineKeyboardButton("❓ QAQ", callback_data="qaq")],
        [InlineKeyboardButton("✅ Чек-листы", callback_data="checklists")],
        [InlineKeyboardButton("🔒 Security Testing", callback_data="security")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info('Пользователь %s (%s) вызвал команду %s', user.username, user.id, text)
    await  update.message.reply_text("📂 Доступные категории статей:", reply_markup=reply_markup)
    logger.info('Отправлено сообщение пользователю %s (%s): "%s"', user.username, user.id, reply_markup)'''