# parsers/rent_ride/get_rentride_car_categories.py

from urllib.parse import urljoin
from utils.selenium_utils import create_chrome_driver_object, get_soup_for_avito_parce


def get_rentride_car_categories(url: str) -> dict:
    """
    Загружает страницу RentRide по указанному URL (через Selenium),
    парсит ссылки на категории автомобилей и возвращает словарь
    вида {Название категории: полный_адрес_ссылки}.
    """
    driver = create_chrome_driver_object(headless=False, proxy=None)
    try:
        soup = get_soup_for_avito_parce(url, driver, attempts=5)

        category_blocks = soup.select('div.car-categories-module a.car-category-preview')

        categories = {}
        for block in category_blocks:
            category_name_elem = block.select_one('.car-type')
            if not category_name_elem:
                continue

            category_name = category_name_elem.get_text(strip=True)
            relative_href = block.get('href', '')

            # Склеиваем домен + относительную ссылку
            full_link = urljoin(url, relative_href)

            categories[category_name] = full_link

        return categories

    finally:
        driver.quit()


# Пример использования:
if __name__ == "__main__":
    url = "https://rentride.ru/"  # Укажите реальную ссылку
    result = get_rentride_car_categories(url)
    for cat, link in result.items():
        print(f"{cat} -> {link}")
