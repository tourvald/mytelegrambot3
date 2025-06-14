import time
import logging
from collections import defaultdict
from aiogram.types import ParseMode
from aiogram.utils.markdown import escape_md
from utils.selenium_utils import create_chrome_driver_object
from utils.google_sheets_utils import get_myphones_spreadsheet
from parsers.avito_parser import get_soup_for_avito_parce, avito_parce_soup

# Настройка логирования
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_convert_to_float(value):
    """Попытка преобразовать строку в число с плавающей запятой. Если не удается – логируем ошибку и возвращаем None."""
    try:
        return float(value)
    except (ValueError, TypeError):
        logging.warning(f"Невозможно преобразовать значение: '{value}' в число!")
        return None

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

    # Создаем драйвер в контекстном менеджере
    with create_chrome_driver_object(headless=True) as driver:
        # Получаем данные из Google Sheets
        myphones = get_myphones_spreadsheet(range=sheet_name)

        # Группируем по ссылке, сохраняя для каждого товара имя (из колонки 0) и коэффициент (колонка 2)
        link_groups = defaultdict(list)
        for myphone in myphones['values']:
            product_name = myphone[0] if len(myphone) > 0 else "Неизвестно"
            key_link = myphone[3] if len(myphone) > 3 else ""
            coef = myphone[2] if len(myphone) > 2 else "1"
            if key_link:
                # Сохраняем кортеж (название товара, коэффициент)
                link_groups[key_link].append((product_name, coef))

        # Обрабатываем каждую уникальную ссылку
        for i, (key_link, items) in enumerate(link_groups.items()):
            # Собираем имена товаров (если их несколько, выводим через запятую)
            product_names = ", ".join({item[0] for item in items})
            position_info = f"({i + 1}/{len(link_groups)})"

            if status_message:
                await status_message.edit_text(
                    f"Парсинг листа '{escape_md(sheet_name)}': позиция {escape_md(position_info)}\n"
                    f"Текущие товары: {escape_md(product_names)}",
                    parse_mode=ParseMode.MARKDOWN_V2
                )

            # Получаем страницу с Avito по ссылке
            soup = get_soup_for_avito_parce(key_link, driver, attempts=5)
            if soup is None:
                print(f"Не удалось загрузить страницу {key_link}. Перезапускаем драйвер.")
                driver.quit()  # Закрываем текущую сессию драйвера
                driver = create_chrome_driver_object(headless=True)  # Создаем новый драйвер
                soup = get_soup_for_avito_parce(key_link, driver, attempts=5)
                if soup is None:
                    print(f"Не удалось загрузить страницу {key_link} даже после перезапуска драйвера.")
                    continue  # Пропускаем этот URL, если повторная попытка не удалась

            av_price, search_request = avito_parce_soup(soup)

            # Приводим av_price к числовому типу
            av_price_numeric = safe_convert_to_float(av_price)
            if av_price_numeric is None:
                print(f"Ошибка: Некорректное значение av_price: {av_price} для ссылки {key_link}")
                continue

            # Для каждого товара с данной ссылкой обрабатываем коэффициент отдельно
            for product_name, coef in items:
                coef_value = safe_convert_to_float(coef)
                if coef_value is None:
                    return_.append(f"Ошибка: Некорректный коэффициент для товара '{product_name}'!")
                    return return_
                sellprice = int(av_price_numeric * coef_value)
                if include_sellprice:
                    return_.append(f'{product_name}, - {av_price_numeric}"/"{sellprice}')
                else:
                    return_.append(f'{product_name}, - {av_price_numeric}')
                sum_av_price += av_price_numeric
                sum_sell_price += sellprice

        if include_sum_av_price:
            return_.append(f'Итогова цена - {sum_av_price}')
        if include_sum_sell_price:
            return_.append(f'Итоговая с коэффициентами  - {sum_sell_price}')

    finish_time = time.perf_counter()
    print(f'Finished in {round(finish_time - start_time, 2)} second(s)')

    # Вывод результата в консоль для отладки
    result_text = "\n".join(return_)
    print("Результат парсинга:\n", result_text)

    return return_