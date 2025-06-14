import re  # Добавьте этот импорт
from aiogram import types
from parsers.youtube_parser import get_youtube_video_info

async def handle_youtube_link(message: types.Message):
    youtube_pattern = re.compile(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+")
    if youtube_pattern.search(message.text):
        await message.reply("Обнаружена ссылка на YouTube. Начинаю обработку...")
        video_info = await get_youtube_video_info(message.text)
        await message.reply(f"Информация о видео: {video_info}")
    else:
        await message.reply("Ссылка не распознана как YouTube.")
        