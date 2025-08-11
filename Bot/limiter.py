import redis
from datetime import datetime, timedelta, timezone

DAILY_LIMIT = 5
ALMATY_TZ = timezone(timedelta(hours=6))

# Подключение к Redis (имя сервиса из docker-compose)
r = redis.Redis(host="redis", port=6379, decode_responses=True)

def _today_key() -> str:
    return datetime.now(ALMATY_TZ).strftime("%Y-%m-%d")

def quota_left(user_id: int) -> int:
    key = f"quota:{user_id}:{_today_key()}"
    used = int(r.get(key) or 0)
    return max(0, DAILY_LIMIT - used)

def can_send_now(user_id: int) -> bool:
    return quota_left(user_id) > 0

def mark_success(user_id: int) -> None:
    key = f"quota:{user_id}:{_today_key()}"
    now = datetime.now(ALMATY_TZ)
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    ttl = int(midnight.timestamp())
    pipe = r.pipeline()
    pipe.incr(key, 1)
    pipe.expireat(key, ttl)  # истекает в полночь Алматы
    pipe.execute()

def time_to_reset_str() -> str:
    now = datetime.now(ALMATY_TZ)
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    delta = midnight - now
    h, r = divmod(delta.seconds, 3600)
    m, _ = divmod(r, 60)
    return f"{h:02d}:{m:02d}"