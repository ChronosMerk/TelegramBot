import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()

@dataclass
class BotConfig:
    tokenTG: str
    tokenDeepSeek: str
    tokenGPT: str
    chat_log: str
    log_dir: str = r'G:\Docker\Log'
    prometheus_port: int = 8000

# Получение и валидация токенов
def get_config() -> BotConfig:
    missing = []

    tokenTG = os.getenv("TOKEN")
    if not tokenTG: missing.append("TOKEN")

    tokenDeepSeek = os.getenv("TOKENDEEPSEEK")
    if not tokenDeepSeek: missing.append("TOKENDEEPSEEK")

    tokenGPT = os.getenv("TOKENGPT")
    if not tokenGPT: missing.append("TOKENGPT")

    if missing:
        raise ValueError(f"❌ Отсутствуют переменные в .env: {', '.join(missing)}")

    # Создание директории для логов
    log_dir = '/app/logs'
    os.makedirs(log_dir, exist_ok=True)

    chat_log = os.getenv("CHATLOG")
    if not tokenTG: missing.append("CHATLOG")

    return BotConfig(
        tokenTG=tokenTG,
        tokenDeepSeek=tokenDeepSeek,
        tokenGPT=tokenGPT,
        chat_log=chat_log,
        log_dir=log_dir,
        prometheus_port=8000
    )

# Импортируем готовую конфигурацию
config = get_config()
