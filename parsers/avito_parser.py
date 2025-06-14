# parsers/avito_parser.py

from utils.selenium_utils import get_soup_for_avito_parce, create_chrome_driver_object
from utils.data_processing import avito_parce_soup
from storage.db import handle_query_and_price  # Импорт функции для работы с базой данных
from datetime import datetime

def parse_avito_link(url):
    """
    Функция для парсинга ссылки на Avito, сохранения данных в базе и возврата средней цены и поискового запроса.
    """
    driver = create_chrome_driver_object(headless=False)
    try:
        soup = get_soup_for_avito_parce(url, driver)
        if soup:
            avg_price, search_request = avito_parce_soup(soup)
            # Записываем данные в базу данных
            handle_query_and_price(search_request, url, avg_price)
            return avg_price, search_request
        else:
            print("Не удалось получить данные с сайта.")
            return None, None
    finally:
        driver.quit()

# Пример использования
if __name__ == "__main__":
    test_url = "https://www.avito.ru/moskva/telefony"  # Вставь сюда тестовую ссылку
    parse_avito_link(test_url)