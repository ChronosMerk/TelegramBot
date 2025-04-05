import pytest
from unittest.mock import AsyncMock, MagicMock
from Bot.handlers.base_Command import QABot

@pytest.mark.asyncio
async def test_start_command():
    # Создаем заглушки
    mock_update = MagicMock()
    mock_context = MagicMock()

    mock_user = MagicMock()
    mock_user.from_user.first_name = "Тест"
    mock_user.from_user.username = "testuser"
    mock_user.from_user.id = 123

    mock_message = AsyncMock()
    mock_message.from_user = mock_user.from_user
    mock_message.text = "/start"
    mock_update.message = mock_message

    # Эмуляция effective_user
    mock_update.effective_user = mock_user.from_user

    bot = QABot()

    # Вызываем метод start
    await bot.start(mock_update, mock_context)

    # Проверяем, что сообщение отправлено
    mock_message.reply_text.assert_called_once_with(
        "Привет, Тест! Я QA-бот, который поможет тебе изучить QA!"
    )