import requests
import logging


class TelegramLogHandler(logging.Handler):
    def __init__(self, token: str, chat_id: str, level=logging.ERROR):
        super().__init__(level)
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🛠 Log:\n{log_entry}"
        }
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"❌ Не удалось отправить лог в Telegram: {e}")