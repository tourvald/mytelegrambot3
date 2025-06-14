from v2root import V2ROOT
import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def get_youtube_video_info(url):
    v2 = V2ROOT()
    v2.set_config_string("vless://CHIK_280592@45.144.54.150:443?type=tcp&security=reality&pbk=564lel2MYjA6mQDGZPA1_fw6TQLVOLuNTPYnyC0d_GY&fp=chrome&sni=whatsapp.com&sid=ffffffffff&spx=%2F#CHIK_280592-🇩🇪Германия")
    v2.start()
    try:
        connector = aiohttp.SocksConnector.from_url('socks5://127.0.0.1:1080')
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    title_element = soup.find('title')
                    if title_element:
                        return title_element.text
                    else:
                        return "Не удалось найти заголовок видео."
                else:
                    return "Не удалось получить информацию о видео."
    finally:
        v2.stop()

if __name__ == '__main__':
    result = asyncio.run(get_youtube_video_info("https://www.youtube.com/shorts/SOXA2PHZwXQ"))
    print(result)
