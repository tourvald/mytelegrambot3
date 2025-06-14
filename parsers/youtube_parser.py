
import aiohttp
from bs4 import BeautifulSoup

async def get_youtube_video_info(url):
    async with aiohttp.ClientSession() as session:
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
        