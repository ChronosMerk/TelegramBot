import requests
from telegram import Update
from telegram.ext import ContextTypes

from Bot.config import config
from Bot.metrics import track_command, track_response_time
from Bot.bot_QA_Logger import log_ai, log_command
from Bot.roles import is_allowed

async def handle_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if not is_allowed(user.id):
        reply_message = "⛔ У тебя нет доступа к этой команде."
        await update.message.reply_text(reply_message)
        log_command(update, reply_message)
        return

    prompt = " ".join(context.args) if context.args else None

    if not prompt:
        reply_message = "❗️Напиши вопрос после команды. Пример: /gpt что такое API?"
        await update.message.reply_text(reply_message)
        log_command(update, reply_message)
        return

    with track_response_time(update.message.text):
        try:
            reply = query_gpt(prompt)
        except Exception as e:
            reply = f"⚠️ Ошибка GPT: {e}"

        await update.message.reply_text(reply)
        track_command(update.message.text)
        log_ai(__name__, user, prompt, reply)

def query_gpt(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.tokenGPT}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
