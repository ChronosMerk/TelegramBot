import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from Bot.config import config

# Настройки yt-dlp для скачивания видео
ydl_opts = {
    'format': 'mp4',
    'outtmpl': 'downloaded_video.%(ext)s',
    'quiet': True
}

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    user = update.effective_user
    username = user.username if user.username else user.first_name

    if url.startswith((
            'https://www.instagram.com/reel/',
            'https://www.tiktok.com/',
            'https://vt.tiktok.com/'
    )):
        print(f"Запрос на скачивание: {url}")

        await context.bot.send_chat_action(chat_id, "upload_video")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_file = ydl.prepare_filename(info)

            # Отправка видео
            with open(video_file, 'rb') as video:
                await context.bot.send_video(
                    chat_id, video,
                    caption=f"🎬 Отправлено пользователем: @{username}"
                )

            # Удаление файла после отправки
            os.remove(video_file)
            await context.bot.delete_message(chat_id, update.message.message_id)

        except Exception as e:
            print(f"Ошибка скачивания: {e}")
            await context.bot.send_message(chat_id, f"⚠️ Поддерживаются только Instagram и TikTok. Отправь нормальную ссылку, а не это: {url[:1000]}")
            # Удаляем неподдерживаемое сообщение
            await context.bot.delete_message(chat_id, update.message.message_id)
