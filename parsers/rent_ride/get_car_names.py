from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.selenium_utils import create_chrome_driver_object
from bs4 import BeautifulSoup

def get_car_names_from_category(url: str, output_file: str) -> list:
    """
    1. Открывает страницу категории (например: https://rentride.ru/arendovat/moskva/economy/)
    2. Находит и кликает по фильтру «Марка»
    3. Собирает все названия марок
    4. Сохраняет их в указанный текстовый файл
    5. Возвращает список названий
    """
    driver = create_chrome_driver_object(headless=True, proxy=None)
    try:
        driver.get(url)

        # Ждём появления кнопки фильтра «Марка»
        marque_filter_trigger = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="filter-label" and contains(text(),"Марка")]/parent::div[@class="filter-trigger"]')
            )
        )
        # Кликаем по фильтру «Марка»
        marque_filter_trigger.click()

        # После клика ждём появления списка .checkbox-list
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.filter-dropdown-holder .checkbox-list'))
        )

        # Берём HTML после клика
        html_after_click = driver.page_source
        soup = BeautifulSoup(html_after_click, 'html.parser')

        # Ищем блок .checkbox-list
        checkbox_list = soup.select_one('.filter-dropdown-holder .checkbox-list')
        if not checkbox_list:
            car_names = []
        else:
            # Собираем названия из .checkbox-label
            labels = checkbox_list.select('label.labeled-round-checkbox.checkbox-list-item .checkbox-label')
            car_names = [label.get_text(strip=True) for label in labels if label.get_text(strip=True)]

        # Сохраняем результат в файл (по одной марке на строку)
        with open(output_file, 'w', encoding='utf-8') as f:
            for name in car_names:
                f.write(name + "\n")

        return car_names

    finally:
        driver.quit()


# Пример использования:
if __name__ == "__main__":
    url = "https://rentride.ru/arendovat/moskva/"
    output_file = "car_brands.txt"
    names = get_car_names_from_category(url, output_file)
    print(f"Список марок (сохранён в {output_file}):")
    print(names)
