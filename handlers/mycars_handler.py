# handlers/mycars_handler.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from services.myphones_service import myphones_get_avarage_prices
import re

def escape_markdown_v2(text: str) -> str:
    # Экранирование специальных символов для Markdown V2
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

async def handle_mycars_command(message: types.Message):
    # Отправляем начальное сообщение
    status_message = await message.reply(f"Начинаю расчет средней стоимости товаров из списка 'mycars'...")

    # Выполняем расчет средней стоимости
    results = await myphones_get_avarage_prices(
        sheet_name="mycars",
        status_message=status_message,
        include_sum_av_price=True,
        include_sellprice=False,
        include_sum_sell_price=False)
    # Экранируем результаты для Markdown V2 и формируем сообщение с результатами
    escaped_results = [escape_markdown_v2(result) for result in results]
    result_message = "\n".join(escaped_results)

    # Отправляем обновленное сообщение с результатами
    await status_message.edit_text(result_message, parse_mode=types.ParseMode.MARKDOWN_V2)

def register_handlers_mycars(dp: Dispatcher):
    dp.register_message_handler(handle_mycars_command, commands=["mycars"])