import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/.."))

@dataclass
class BotConfig:
    tokenTG: str
    tokenDeepSeek: str
    tokenGPT: str
    chat_log: str
    thread_id: int
    allowed_users: set
    allowed_chats: set
    log_dir: str = r'/app/logs'
    cookies_path: str = os.path.join(ROOT_DIR, 'cookies', 'instagram.txt')
    prometheus_port: int = 8000

def get_config() -> BotConfig:
    missing = []

    tokenTG = os.getenv("TOKEN")
    if not tokenTG: missing.append("TOKEN")

    tokenDeepSeek = os.getenv("TOKENDEEPSEEK")
    if not tokenDeepSeek: missing.append("TOKENDEEPSEEK")

    tokenGPT = os.getenv("TOKENGPT")
    if not tokenGPT: missing.append("TOKENGPT")

    chat_log = os.getenv("CHATLOG")
    if not chat_log: missing.append("CHATLOG")

    thread_id = os.getenv("THREAD_ID")
    if not thread_id: missing.append("THREAD_ID")

    raw_ids = os.getenv("ALLOWED_USERS")
    if not raw_ids:
        missing.append("ALLOWED_USERS")
        allowed_users = set()
    else:
        allowed_users = set(map(int, raw_ids.replace(",", " ").split()))

    raw_ids_chat = os.getenv("ALLOWED_CHAT")
    if not raw_ids_chat:
        missing.append("ALLOWED_CHAT")
        allowed_chats = set()
    else:
        allowed_chats = set(map(int, raw_ids_chat.replace(",", " ").split()))

    if missing:
        raise ValueError(f"❌ Отсутствуют переменные в .env: {', '.join(missing)}")

    # Создание директории логов (если нужно)
    os.makedirs('/app/logs', exist_ok=True)

    return BotConfig(
        tokenTG=tokenTG,
        tokenDeepSeek=tokenDeepSeek,
        tokenGPT=tokenGPT,
        chat_log=chat_log,
        thread_id=thread_id,
        allowed_users=allowed_users,
        allowed_chats=allowed_chats
    )

# Готовый конфиг
config = get_config()
