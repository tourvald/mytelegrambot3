# handlers/myproperty_handler.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from services.myphones_service import myphones_get_avarage_prices
import re
import asyncio


def escape_markdown_v2(text: str) -> str:
    # Экранирование специальных символов для Markdown V2
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


async def handle_myproperty_command(message: types.Message):
    status_message = await message.reply("Начинаю расчет средней стоимости товаров из списка 'myproperty'...")
    results = await myphones_get_avarage_prices(sheet_name="myproperty", status_message=status_message)

    # Экранируем специальные символы в результатах
    escaped_results = [escape_markdown_v2(result) for result in results]

    # Объединение всех результатов в одно сообщение и отправка пользователю
    result_message = "\n".join(escaped_results)
    await status_message.edit_text(result_message, parse_mode=types.ParseMode.MARKDOWN_V2)


def register_myproperty_handler(dp: Dispatcher):
    dp.register_message_handler(handle_myproperty_command, commands=['myproperty'])