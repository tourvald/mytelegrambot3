import os
import time
import random
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

def get_headings_and_save_html(url, driver, attempts=5, initial_delay=5, delay_increment=2):
    """
    Функция открывает страницу по URL, ждёт появления заголовков H1/H2/H3,
    сохраняет HTML-код страницы в файл page.html и возвращает тексты всех H1, H2, H3.
    """
    delay = initial_delay

    for attempt in range(attempts):
        try:
            logging.info(f"Попытка {attempt + 1} из {attempts} для {url}")
            driver.get(url)

            # Рандомная задержка для эмуляции поведения реального пользователя
            time.sleep(random.uniform(delay, delay + 2))

            # Ждём появления хотя бы одного заголовка (H1, H2, H3) в течение 5 секунд
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //h3"))
                )
            except TimeoutException:
                logging.warning("Заголовки H1, H2, H3 не найдены. Пробуем обновить страницу.")
                driver.refresh()
                continue

            # Получаем HTML
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Извлекаем тексты H1, H2, H3
            h1_texts = [elem.get_text(strip=True) for elem in soup.find_all('h1')]
            h2_texts = [elem.get_text(strip=True) for elem in soup.find_all('h2')]
            h3_texts = [elem.get_text(strip=True) for elem in soup.find_all('h3')]

            # Сохраняем HTML в файл page.html рядом со скриптом
            file_path = os.path.join(os.path.dirname(__file__), "page.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

            logging.info(f"HTML-код страницы сохранён в {file_path}")
            return h1_texts, h2_texts, h3_texts

        except Exception as e:
            logging.error(f"Ошибка на попытке {attempt + 1} для {url}: {e}")
            delay += delay_increment

    logging.error(f"Не удалось получить заголовки после {attempts} попыток.")
    return None, None, None


# Пример использования:
if __name__ == "__main__":
    from selenium import webdriver

    # Инициализация драйвера (Chrome, Firefox и т.д.)
    driver = webdriver.Chrome()

    test_url = "https://rentride.ru"
    h1_list, h2_list, h3_list = get_headings_and_save_html(test_url, driver)

    if h1_list or h2_list or h3_list:
        logging.info("Заголовки успешно получены!")
        logging.info(f"H1: {h1_list}")
        logging.info(f"H2: {h2_list}")
        logging.info(f"H3: {h3_list}")
    else:
        logging.warning("Не удалось получить заголовки.")

    driver.quit()
