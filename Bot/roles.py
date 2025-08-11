from Bot.config import config

#доступ по чатам
def is_allowed_chat(chat_id: int) -> bool:
    return chat_id in config.allowed_chats

#блокировка пользователей
def is_banned_user(user_id: int) -> bool:
    return int(user_id) in config.banned_users