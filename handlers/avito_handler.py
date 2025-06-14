import re  # Добавьте этот импорт
from aiogram import types
from parsers.avito_parser import parse_avito_link

async def handle_avito_link(message: types.Message):
    avito_pattern = re.compile(r"(https?://)?(www\.)?avito\.ru/")
    if avito_pattern.search(message.text):
        await message.reply("Обнаружена ссылка на Avito. Начинаю парсинг данных...")
        parsed_data = parse_avito_link(message.text)
        await message.reply(f"Средняя цена: {parsed_data[0]}\nПоиск: {parsed_data[1]}")
    else:
        await message.reply("Ссылка не распознана как Avito.")