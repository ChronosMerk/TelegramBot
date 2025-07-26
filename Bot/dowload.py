import logging
import os
import requests
from bs4 import BeautifulSoup
from config import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    filename='logs.log', filemode='a',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


INSTAGRAM_URL = os.getenv("INSTAGRAM_URL")
TIKTOK_URL = os.getenv("TIKTOK_URL")
YOUTUBE_URL = os.getenv("YOUTUBE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Единая функция для отправки видео
async def send_video(chat_id, video_content, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id, 'upload_video')
    await context.bot.send_video(chat_id, video_content)

# Обработка TikTok
async def handle_tiktok(url, chat_id, context):
    data = {'q': url, 'lang': 'en'}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        res = requests.post(TIKTOK_URL, data=data, headers=headers).json()
        soup = BeautifulSoup(res['data'], 'html.parser')
        video_tag = soup.find('video')
        video_url = video_tag['data-src']
        video = requests.get(video_url).content
        await send_video(chat_id, video, context)
    except Exception as e:
        logger.error(f"TikTok error: {e}")
        await context.bot.send_message(chat_id, "Ошибка загрузки видео с TikTok.")

# Обработка Instagram
async def handle_instagram(url, chat_id, context):
    data = {'url': url, 'lang_code': 'en'}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        res = requests.post(INSTAGRAM_URL, data=data, headers=headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            first_a = soup.find('a')
            if first_a:
                video_url = first_a['href']
                video = requests.get(video_url).content
                await send_video(chat_id, video, context)
            else:
                await context.bot.send_message(chat_id, "Видео не найдено.")
        else:
            await context.bot.send_message(chat_id, "Ошибка запроса к Instagram.")
    except Exception as e:
        logger.error(f"Instagram error: {e}")
        await context.bot.send_message(chat_id, "Ошибка загрузки видео с Instagram.")

# Обработка YouTube
async def handle_youtube(url, chat_id, context):
    try:
        res = requests.get(f'{YOUTUBE_URL}?url={url}').json()
        video_url = res['data']['video_formats'][0]['url']
        video = requests.get(video_url).content
        await send_video(chat_id, video, context)
    except Exception as e:
        logger.error(f"YouTube error: {e}")
        await context.bot.send_message(chat_id, "Ошибка загрузки видео с YouTube.")

# Главный обработчик сообщений
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    logger.info(f"Запрос от {chat_id}: {url}")

    if url.startswith(('https://vt.tiktok.com/', 'https://www.tiktok.com')):
        await handle_tiktok(url, chat_id, context)
    elif url.startswith('https://www.instagram.com/'):
        await handle_instagram
