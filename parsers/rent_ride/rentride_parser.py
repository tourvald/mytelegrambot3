import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

# Ваши утилиты Selenium
from utils.selenium_utils import create_chrome_driver_object

def get_random_delay() -> float:
    """Возвращает случайное число секунд (от 3 до 7) для имитации «человеческих» пауз."""
    return random.uniform(3, 7)

class RentRideParser:
    """
    Класс, инкапсулирующий логику навигации по rentride.ru.
    Использует один Selenium-драйвер на весь жизненный цикл объекта.
    """

    def __init__(self, headless: bool = True):
        """Создаём драйвер, задаём базовый URL."""
        self.driver = create_chrome_driver_object(headless=headless, proxy=None)
        self.base_url = "https://rentride.ru/arendovat/moskva/"
        self.wait = WebDriverWait(self.driver, 15)

    def open_main_page(self):
        """Открываем главную страницу аренды в Москве."""
        self.driver.get(self.base_url)
        # Немного ждём, пока страница полностью загрузится
        time.sleep(get_random_delay())

    def check_page_loaded(self) -> bool:
        try:
            time.sleep(5)  # на всякий случай
            labels = self.driver.find_elements(By.CLASS_NAME, "filter-label")
            print(f"Найдено {len(labels)} элементов с классом 'filter-label':")
            for label in labels:
                print("-", label.text.strip())
            return any("Марка" in label.text for label in labels)
        except Exception as e:
            print("Ошибка при поиске фильтров:", e)
            return False

    def select_brand(self, brand_name: str):
        """
        Кликает по фильтру «Марка» и выбирает заданную марку.
        """
        # Открываем меню «Марка»
        brand_filter_trigger = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[contains(@class, "car-filter") and .//div[contains(@class, "filter-label") and normalize-space(text())="Марка"]]/div[contains(@class, "filter-trigger")]')
            )
        )
        time.sleep(get_random_delay())  # случайная пауза
        brand_filter_trigger.click()

        # Ждём, пока появится список марок
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.filter-dropdown-holder .checkbox-list')))

        # Находим нужную марку по тексту
        brand_xpath = (
            f'//div[contains(@class, "filter-dropdown-holder")]'
            f'//label[contains(@class, "labeled-round-checkbox") and '
            f'.//span[contains(@class, "checkbox-label") and normalize-space(text())="{brand_name}"]]'
        )
        brand_elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, brand_xpath)))
        time.sleep(get_random_delay())  # ещё одна пауза
        brand_elem.click()

        # Возможно, страница подгружает предложения. Подождём чуть-чуть
        time.sleep(get_random_delay())

    def select_model(self, model_name: str):
        print(f"[select_model] Кликаем по фильтру 'Модель'")
        model_filter_xpath = (
            '//div[contains(@class, "car-filter") and .//div[contains(@class, "filter-label") and normalize-space(text())="Модель"]]/div[contains(@class, "filter-trigger")]'
        )
        model_filter_trigger = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, model_filter_xpath))
        )
        print(f"[select_model] Найден фильтр 'Модель', кликаем...")
        time.sleep(get_random_delay())
        model_filter_trigger.click()
        print(f"[select_model] Клик по 'Модель' выполнен, ждем появления выпадашки")

        try:
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.car-filter.UniversalCarFilter.opened .car-filter-select-list'))
            )
            print("[select_model] Выпадающий список моделей появился")
        except Exception:
            raise Exception("Выпадающий список моделей не появился после клика. Проверьте верность XPATH/CSS или задержку.")

        time.sleep(get_random_delay())
        # Для дебага: делаем скриншот открытой выпадашки
        self.driver.save_screenshot(f"debug_dropdown_{model_name}.png")

        model_xpath = (
            '//div[contains(@class, "car-filter-select-list")]'
            '//span[contains(@class, "checkmark-label-text") and contains(., "{}")]'.format(model_name)
        )
        print(f"[select_model] Ищем модель '{model_name}' по XPATH: {model_xpath}")
        model_elem = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, model_xpath))
        )
        print(f"[select_model] Модель '{model_name}' найдена, кликаем...")
        time.sleep(get_random_delay())
        model_elem.click()
        print(f"[select_model] Клик по модели '{model_name}' выполнен")
        self.driver.save_screenshot(f"debug_model_{model_name}.png")
        time.sleep(get_random_delay())

    def get_all_brands(self) -> list:
        brand_filter_trigger = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, '//div[contains(@class, "car-filter") and .//div[contains(@class, "filter-label") and normalize-space(text())="Марка"]]/div[contains(@class, "filter-trigger")]'
        )))
        time.sleep(get_random_delay())
        brand_filter_trigger.click()
        self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '.filter-dropdown-holder .checkbox-list'
        )))
        labels = self.driver.find_elements(By.CSS_SELECTOR, '.checkbox-list .checkbox-label')
        brand_names = [label.text.strip() for label in labels if label.text.strip()]
        brand_filter_trigger.click()
        return brand_names

    def get_models_for_selected_brand(self) -> list:
        filter_xpath = '//div[contains(@class, "car-filter") and .//div[contains(@class, "filter-label") and normalize-space(text())="Модель"]]/div[contains(@class, "filter-trigger")]'
        model_filter_trigger = self.wait.until(EC.element_to_be_clickable((By.XPATH, filter_xpath)))
        time.sleep(get_random_delay())
        model_filter_trigger.click()
        self.wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '.car-filter.UniversalCarFilter.opened .car-filter-select-list'
        )))
        time.sleep(get_random_delay())
        elements = self.driver.find_elements(By.CSS_SELECTOR, '.car-filter-select-list .checkmark-label-text')
        models = [e.text.strip() for e in elements if e.text.strip()]
        model_filter_trigger.click()
        return models

    def parse_prices(self) -> list:
        """
        Собирает цены из списка объявлений на текущей странице.
        Возвращает список (или что угодно: среднюю цену, словарь и т.д.).
        """
        # Берём HTML
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Допустим, на карточках есть класс .car-card, а цены хранятся в каком-то .car-price
        # Примерный поиск:
        cards = soup.select('.car-card')  # Нужно подкорректировать под реальный DOM

        prices = []
        for card in cards:
            price_elem = card.select_one('.car-price')
            if price_elem:
                # Нужно парсить строку (например, "от 1590 ₽" → 1590)
                text = price_elem.get_text(strip=True)
                # Допустим, убираем все не-цифры, кроме пробела
                # Это сильно зависит от формата цены
                import re
                match = re.search(r'(\d+)', text)
                if match:
                    prices.append(int(match.group(1)))

        return prices

    def close(self, delay: float = 5.0):
        """Закрываем драйвер с паузой (по умолчанию 5 сек), чтобы успеть увидеть результат."""
        time.sleep(delay)
        self.driver.quit()

if __name__ == "__main__":
    parser = RentRideParser(headless=False)
    parser.open_main_page()
    time.sleep(25)  # увеличиваем задержку для полной загрузки
    parser.driver.save_screenshot('debug_rentride.png')

    print(parser.driver.current_url)
    if not parser.check_page_loaded():
        print("Не удалось найти фильтр «Марка» на странице.")
    else:
        import csv

        all_data = []

        brands = parser.get_all_brands()
        print(f"Найдено {len(brands)} марок")

        for brand in brands:
            try:
                parser.select_brand(brand)
                models = parser.get_models_for_selected_brand()
                print(f"{brand}: найдено {len(models)} моделей")

                for model in models:
                    try:
                        parser.select_model(model)
                        prices = parser.parse_prices()
                        avg_price = round(sum(prices)/len(prices), 2) if prices else None
                        all_data.append((brand, model, avg_price, len(prices)))
                        print(f"{brand} {model} — {avg_price} ₽ ({len(prices)} шт.)")
                    except Exception as e:
                        print(f"[!] Не удалось обработать модель {model} ({brand}): {e}")
            except Exception as e:
                print(f"[!] Не удалось обработать марку {brand}: {e}")

        with open("rentride_prices.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Бренд", "Модель", "Средняя цена", "Количество"])
            writer.writerows(all_data)

    parser.close(delay=10.0)
