ALLOWED_USERS = {
    468056370,
}

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS
