# services/myphones_service.py

import time
from utils.selenium_utils import create_chrome_driver_object
from utils.google_sheets_utils import get_myphones_spreadsheet
from parsers.avito_parser import get_soup_for_avito_parce, avito_parce_soup
import asyncio
from aiogram.types import ParseMode
from aiogram.utils.markdown import escape_md

async def myphones_get_avarage_prices(
    sheet_name="myphones",
    status_message=None,
    include_sum_sell_price=True,
    include_sum_av_price=True,
    include_sellprice=True
):
    start_time = time.perf_counter()
    sum_av_price = 0
    sum_sell_price = 0
    return_ = []

    # Создание драйвера в контекстном менеджере
    with create_chrome_driver_object(headless=True) as driver:
        # Используем sheet_name для получения данных
        myphones = get_myphones_spreadsheet(range=sheet_name)  # Заменили range= на sheet_name

        for i, myphone in enumerate(myphones['values']):
            # Получение названия позиции и ссылки из строки
            item_name = myphone[0] if len(myphone) > 0 else "Неизвестно"  # Название позиции
            key_link = myphone[3] if len(myphone) > 3 else ""  # Ссылка для парсинга
            index = myphone[2] if len(myphone) > 2 else "1"  # Индекс для расчета цены

            # Экранирование названия позиции и других данных для корректного отображения в Markdown V2
            escaped_item_name = escape_md(item_name)
            position_info = f"({i + 1}/{len(myphones['values'])})"

            # Обновление статуса перед каждым парсингом
            if status_message:
                await status_message.edit_text(
                    f"Парсинг листа '{escape_md(sheet_name)}': позиция {escape_md(position_info)}\n"
                    f"Текущая позиция: {escaped_item_name}",
                    parse_mode=ParseMode.MARKDOWN_V2
                )

            # Получение данных с Avito
            if key_link:
                soup = get_soup_for_avito_parce(key_link, driver, attempts=5)
                av_price, key = avito_parce_soup(soup)
            else:
                av_price = 0  # Если ссылка пустая, то цена = 0

            # Расчет цены продажи
            sellprice = int(av_price * float(index))

            # Формирование результата в зависимости от параметров
            if include_sellprice:
                return_.append(f'{item_name}, - {av_price}"/"{sellprice}')
            else:
                return_.append(f'{item_name}, - {av_price}')

            sum_av_price += av_price
            sum_sell_price += sellprice

        # Добавление общей суммы цен в зависимости от параметров
        if include_sum_av_price:
            return_.append(f'Итогова цена - {sum_av_price}')
        if include_sum_sell_price:
            return_.append(f'Итоговая с коэффициентами  - {sum_sell_price}')

    finish_time = time.perf_counter()
    print(f'Finished in {round(finish_time - start_time, 2)} second(s)')

    return return_