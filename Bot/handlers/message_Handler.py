from telegram import Update
from telegram.ext import ContextTypes

from Bot.bot_QA_Logger import log_command
from logging_project.metrics import track_command, track_response_time


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
    with track_response_time(query.data):
        reply_text = category_map.get(query.data, "❌ Неизвестная категория")
        await query.edit_message_text(text=reply_text)
        log_command(update, reply_text)
        track_command(query.data)