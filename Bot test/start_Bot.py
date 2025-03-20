from base_Command import QABot
from bot_QA_Logger import logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Обработчик кнопок категорий
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category_map = {
        "manual": "📌 Manual QA — статьи о ручном тестировании.",
        "automation": "🤖 Automation QA — статьи по автоматизации тестирования.",
        "tools": "🛠 Инструменты — Postman, Selenium, JMeter и другие.",
        "methodologies": "📚 Методологии — Agile, Scrum, Waterfall.",
        "qaq": "❓ QAQ — Вопросы и ответы на собеседования.",
        "checklists": "✅ Чек-листы — стандарты тестирования.",
        "security": "🔒 Security Testing — тестирование безопасности.",
    }

    reply_text = category_map.get(query.data, "❌ Неизвестная категория")
    await query.edit_message_text(text=reply_text)

    logger.info("Пользователь выбрал категорию: %s", query.data)
    logger.info("Отправлено сообщение пользователю %s (%s): %s", query.from_user.username, query.id,reply_text)

# Обработчик неизвестных команд и сообщений
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    logger.info('Пользователь %s (%s) вызвал команду %s', user.username, user.id, text)
    reply_message = "Извини, я не понимаю эту команду."

    await update.message.reply_text(reply_message)
    logger.warning('Неизвестное сообщение от %s (%s): "%s"', user.username, user.id, text)
'''def main():
    app = ApplicationBuilder().token(tokenTG).build()

    # Обработчик нажатий на кнопки
    app.add_handler(CallbackQueryHandler(button_handler))

    # Неизвестные команды и текстовые сообщения (всегда последними!)
    app.add_handler(MessageHandler(filters.COMMAND, unknown_message))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown_message))

    logger.info('Все завилось, Проверяй')
    app.run_polling()
    '''

if __name__ == "__main__":
    bot = QABot()  # Создаём объект бота
    bot.run()  # Запускаем бота
