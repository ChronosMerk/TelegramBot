import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pyexpat.errors import messages

# Загрузка .env
load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/.."))

@dataclass
class BotConfig:
    tokenTG: str
    thread_id: int
    allowed_users: set
    allowed_chats: set
    banned_users: set
    log_dir: str = r'/app/logs'


def get_config() -> BotConfig:
    missing = []

    tokenTG = os.getenv("TOKEN")
    if not tokenTG: missing.append("TOKEN")

    thread_id = os.getenv("THREAD_ID")
    if not thread_id: missing.append("THREAD_ID")

    def parse_id_set(env_name: str, required: bool = True) -> set[int]:
        raw = os.getenv(env_name)
        if not raw:
            if required:
                missing.append(env_name)
            return set()
        return set(map(int, raw.replace(",", " ").split()))

    allowed_users = parse_id_set("ALLOWED_USERS")
    banned_users = parse_id_set("BANNED_USER", required=False)
    allowed_chats = parse_id_set("ALLOWED_CHAT")

    if missing:
        raise ValueError(f"❌ Отсутствуют переменные в .env: {', '.join(missing)}")

    # Создание директории логов (если нужно)
    os.makedirs('/app/logs', exist_ok=True)

    return BotConfig(
        tokenTG=tokenTG,
        thread_id=int(thread_id),
        allowed_users=allowed_users,
        allowed_chats=allowed_chats,
        banned_users=banned_users
    )

# Готовый конфиг
config = get_config()
