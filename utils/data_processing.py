
import numpy as np
import re

def avito_parce_soup(soup):
    price_list = []
    search_input = soup.find('input', {'data-marker': 'search-form/suggest/input'})
    if search_input:
        search_request = search_input.get('value')
    else:
        search_request = "Не найдено название запроса"

    div_catalog_serp = soup.find('div', {'data-marker': 'catalog-serp'})
    if div_catalog_serp:
        for price in div_catalog_serp.find_all('meta', {'itemprop': 'price'}):
            price_list.append(price.get('content'))
    if len(price_list) > 1:
        try:
            av_price_std = av_price_sdt(price_list)
        except Exception as e:
            av_price_std = "Ошибка вычисления"
    else:
        av_price_std = "Цен не обнаружено"

    return av_price_std, search_request.lower()

def av_price_sdt(price_list):
    price_list = sorted(int(i) for i in price_list if re.fullmatch(r'\d+', i))
    price_list = price_list[int(len(price_list) * 0.1):len(price_list) - int(len(price_list) * 0.1)]
    price_list_std = int(np.std(price_list))
    price_list_to_remove_right = len(price_list) - 1
    price_list_to_remove_left = 0
    for i in range(len(price_list) // 2, 0, -1):
        if price_list[i] - price_list[i - 1] > price_list_std:
            price_list_to_remove_left = i
            break

    for i in range(len(price_list) // 2, len(price_list), 1):
        if price_list[i] - price_list[i - 1] > price_list_std:
            price_list_to_remove_right = i - 1
            break
    if len(price_list) > 5:
        if len(price_list[price_list_to_remove_left:price_list_to_remove_right]) > 2:
            price_list = price_list[price_list_to_remove_left:price_list_to_remove_right]

    av_price = int(np.average(price_list))
    return av_price
        