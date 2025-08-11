import os
import yt_dlp
from telegram import Update
from telegram.ext import ContextTypes
from Bot.roles import is_allowed_chat, is_banned_user
from Bot.config import BotConfig

# Настройки yt-dlp для скачивания видео
ydl_opts = {
    'format': 'mp4',
    'outtmpl': r'downloaded_video.%(ext)s',
    'quiet': True
}
ALLOWED_URLS = (
    'https://www.instagram.com/reel/',
    'https://www.tiktok.com/',
    'https://vt.tiktok.com/',
    'https://vm.tiktok.com/',
)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    message_thread_id = 7147
    special_group_id = -1002240938626
    user = update.effective_user
    user_id = update.effective_user.id
    username = user.username if user.username else user.first_name
    username_resent = update.message.api_kwargs.get("forward_from")

    if is_banned_user(user_id):
        await update.message.reply_text(f"⛔ Вы заблокированы. @{username}")
        await context.bot.delete_message(chat_id, update.message.message_id)
        return

    if is_allowed_chat(chat_id):
        if url.startswith(ALLOWED_URLS):
            print(f"Запрос на скачивание: {url}")
            message_to_telegram = f"🎬 Отправлено пользователем: @{username}"

            if username_resent:
                message_to_telegram += f"\n📌 Переслано от пользователя: @{username_resent.get('username') or username_resent.get('first_name')}"

            message_to_telegram += f"\n🌐 Ссылка: {url[:1000]}"

            if chat_id == special_group_id:
                thread_id = message_thread_id
            else:
                thread_id = update.message.message_thread_id

            await context.bot.send_chat_action(chat_id, "upload_video")

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_file = ydl.prepare_filename(info)

                # Отправка видео
                with open(video_file, 'rb') as video:
                    await context.bot.send_video(
                        chat_id,
                        video,
                        caption=message_to_telegram,
                        **({'message_thread_id': thread_id} if thread_id else {})
                    )

                # Удаление файла после отправки
                os.remove(video_file)
                await context.bot.delete_message(chat_id, update.message.message_id)

            except Exception as e:
                error_text = str(e)
                print(f"Ошибка скачивания: {error_text}")
                if 'photo' in error_text:
                    pass
                elif 'You must be 18 years old' in error_text:
                    await context.bot.send_message(chat_id, f"🚫Ошибка, контент 18+. БОЛЬШЕ НЕТ ДОСТУПА \n```{str(e)}```", parse_mode="Markdown")
                else:
                    print(f"Ошибка скачивания: {error_text}")
                    await context.bot.send_message(chat_id, f"⚠️ Поддерживаются только Instagram и TikTok. Отправь @{username} нормальную ссылку, а не это: {url[:1000]} \n Ошибка: ```{str(e)}```", parse_mode="Markdown")
                    # Удаляем неподдерживаемое сообщение
                    await context.bot.delete_message(chat_id, update.message.message_id)
