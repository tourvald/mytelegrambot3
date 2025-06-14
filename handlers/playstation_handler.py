# handlers/playstation_handler.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from services.myphones_service import myphones_get_avarage_prices
import re
import asyncio

def escape_markdown_v2(text: str) -> str:
    # Экранирование специальных символов для Markdown V2
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

async def handle_playstation_command(message: types.Message):
    status_message = await message.reply("Начинаю расчет средней стоимости товаров из списка 'playstation'...")
    results = await myphones_get_avarage_prices(sheet_name="playstation", status_message=status_message)

    # Экранирование результатов для Markdown V2
    escaped_results = [escape_markdown_v2(result) for result in results]
    result_message = "\n".join(escaped_results)

    await status_message.edit_text(result_message, parse_mode=types.ParseMode.MARKDOWN_V2)

def register_playstation_handler(dp: Dispatcher):
    dp.register_message_handler(handle_playstation_command, commands=['playstation'])