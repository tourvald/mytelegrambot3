import requests
from bs4 import BeautifulSoup

# Получение списка бесплатных http/https прокси с сайта
def get_free_proxies():
    """Возвращает список прокси из таблицы на free-proxy-list.net."""
    url = "https://free-proxy-list.net/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # На сайте таблица может иметь разные атрибуты, поэтому ищем несколько вариантов
    table = soup.find("table", id="proxylisttable")
    if not table:
        proxy_div = soup.find("div", class_="fpl-list")
        if proxy_div:
            table = proxy_div.find("table")

    if not table:
        print(
            "Не удалось найти таблицу с прокси! Проверь источник или сайт заблокирован."
        )
        return []

    rows = table.tbody.find_all("tr") if table.tbody else table.find_all("tr")
    proxies = []
    for row in rows:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        # Строки таблицы должны содержать не менее 7 ячеек: IP, порт и флаг Https
        if len(cells) < 7:
            continue

        ip = cells[0]
        port = cells[1]
        https = cells[6].lower().startswith("yes")
        scheme = "https" if https else "http"
        proxies.append(f"{scheme}://{ip}:{port}")

    return proxies

# Проверка — можно ли через прокси достучаться до YouTube
def is_proxy_working(proxy_url):
    try:
        response = requests.get(
            "https://www.youtube.com/",
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=7
        )
        # Если 200 — рабочий
        return response.status_code == 200
    except Exception:
        return False

if __name__ == "__main__":
    print("Ищем бесплатные прокси...")
    proxies = get_free_proxies()
    print(f"Найдено {len(proxies)} https прокси, начинаю тестировать...")
    working_proxies = []
    for proxy in proxies:
        print(f"Пробуем: {proxy}")
        if is_proxy_working(proxy):
            print(f"Рабочий прокси: {proxy}")
            working_proxies.append(proxy)
            # Можно сделать break если нужен только один
            break
    if not working_proxies:
        print("Не найдено рабочих прокси.")
    else:
        print("Вот рабочий прокси:", working_proxies[0])
