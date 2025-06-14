
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller


def create_chrome_driver_object(headless=True, proxy=None):
    chromedriver_autoinstaller.install()  # Автоматически устанавливает соответствующий ChromeDriver

    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'  # Попробуйте также 'normal' для полного ожидания загрузки
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--ignore-ssl-errors')
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Установка времени ожидания загрузки страницы
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)  # Увеличение тайм-аута до 60 секунд

    return driver

def get_soup_for_avito_parce(url, driver, attempts=5):
    delay = 5  # Начальная задержка
    for attempt in range(attempts):
        try:
            driver.get(url)

            # Рандомная задержка (эмуляция человеческого поведения)
            time.sleep(random.uniform(delay, delay + 2))

            # Проверка на наличие заголовков H1, H2, H3 в течение 5 секунд
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //h3"))
                )
            except TimeoutException:
                # Обновляем страницу, если заголовки не были найдены в течение 5 секунд
                print(f"Попытка {attempt + 1}: заголовки H1, H2, H3 не найдены, обновление страницы.")
                driver.refresh()
                continue  # Пробуем снова

            # Проверка на блокировку по IP или загрузку страницы
            h2_elements = driver.find_elements(By.TAG_NAME, "h2")
            h2_texts = [element.text for element in h2_elements]
            if "Доступ ограничен: проблема с IP" in h2_texts or "Подождите, идет загрузка" in h2_texts:
                print(f"Попытка {attempt + 1} для {url}: Обнаружена блокировка или проблема с загрузкой. Пробуем снова через {delay} секунд...")
                delay += 2  # Увеличиваем задержку
                continue  # Пробуем еще раз

            # Получаем HTML страницы и создаем объект BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            return soup

        except Exception as e:
            print(f"Произошла ошибка на попытке {attempt + 1} для {url}: {e}")
            delay += 2  # Увеличиваем задержку
            continue  # Пробуем еще раз

    # Если после всех попыток не удалось получить содержимое
    print(f"Не удалось загрузить страницу {url} корректно после всех попыток.")
    return None
        