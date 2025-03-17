from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bot_QA_Logger import logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    logger.info('Пользователь %s (%s) вызвал команду %s', user.username, user.id, text)
    reply_message = f"Привет, {user.first_name}! Я QA-бот, который поможет тебе изучить QA! Для помощи напишите /help В стадии разработки"
    await update.message.reply_text(reply_message)

    logger.info('Отправлено сообщение пользователю %s (%s): "%s"', user.username, user.id, reply_message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    logger.info('Пользователь %s (%s) вызвал команду %s', user.username, user.id, text)
    reply_message = "Основные команды бота: \n/start — приветствие и описание возможностей бота. \n/help — краткая инструкция по использованию и список доступных команд. \n/categories — отображение списка категорий (например, «Manual QA», «Automation QA», «Инструменты», «Методологии», «QAQ» и т.д.)."
    await  update.message.reply_text(reply_message)

    logger.info('Отправлено сообщение пользователю %s (%s): "%s"', user.username, user.id, reply_message)

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    logger.info('Отправлено сообщение пользователю %s (%s): "%s"', user.username, user.id, reply_markup)