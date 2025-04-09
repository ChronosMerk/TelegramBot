# ✅ Makefile для управления проектом Telegram-бота + Docker + Тесты

# 📦 Python-бекенд
run:
	python Bot/start_Bot.py

pytest:
	PYTHONPATH=. pytest tests/ --disable-warnings -v

test: pytest

# 🐳 Docker
up:
	cd Docker && docker-compose up -d --build

down:
	cd Docker && docker-compose down

logs:
	cd Docker && docker-compose logs -f bot

bash:
	docker exec -it telegram_bot sh

clean:
	docker system prune -a -f

# 📁 Логи
logs-dir:
	ls -l G:/Docker/Log

# 🧹 Очистка логов проекта (локально)
clear-logs:
	rm -f G:/Docker/Log/*.log || true

# 📈 Графана
grafana:
	echo "http://localhost:3000"

prometheus:
	echo "http://localhost:9090"

# 🔁 Обновление зависимостей
requirements:
	pip install -r requirements.txt
