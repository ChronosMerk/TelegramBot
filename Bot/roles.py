ALLOWED_USERS = {
    468056370,
}

ALLOWED_CHAT = {
    -1002240938626
}
#доступ user
def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS
#доступ по чатам
def is_allowed_chat(chat_id: int) -> bool:
    return chat_id in ALLOWED_CHAT