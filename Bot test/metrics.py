from prometheus_client import Counter, Histogram, start_http_server
from config import prometheus_port

# Счётчик количества команд
commands_total = Counter('telegram_bot_commands_total', 'Количество вызовов команд', ['command'])

# Гистограмма времени отклика
response_time = Histogram('telegram_bot_response_seconds', 'Время ответа на команду', ['command'])

# Запускаем HTTP-сервер для метрик на порту 8000
start_http_server(prometheus_port)

#Очистка команд
def normalize_command(cmd: str) -> str:
    allowed = ["/start", "/help", "/categories"]
    for command in allowed:
        if cmd.startswith(command):
            return command
    return "unknown"


# Вспомогательные функции
def track_command(command_name):
    command_name = normalize_command(command_name)
    commands_total.labels(command=command_name).inc()

def track_response_time(command_name):
    command_name = normalize_command(command_name)
    return response_time.labels(command=command_name).time()  # как декоратор или context manager