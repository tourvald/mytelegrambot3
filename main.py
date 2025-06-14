# main.py

from aiogram import Bot, Dispatcher, executor
from handlers import (
    avito_handler,
    youtube_handler,
    playstation_handler,
    myproperty_handler,
    mycars_handler
)
from dotenv import load_dotenv
import os
import platform
from storage.db import initialize_database  # Импортируем функцию для инициализации базы данных

# Загрузка переменных окружения из файла .env
load_dotenv(dotenv_path='config/.env')

# Определение токена в зависимости от операционной системы
if platform.system() == "Windows":
    API_TOKEN = os.getenv('BOT_TOKEN_WIN')
else:
    API_TOKEN = os.getenv('BOT_TOKEN')

# Проверка наличия токена
if not API_TOKEN:
    raise ValueError("Не удалось найти действующий токен для текущей операционной системы.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инициализация базы данных
initialize_database()

# Регистрация хендлеров
dp.register_message_handler(avito_handler.handle_avito_link, lambda message: 'avito' in message.text)
dp.register_message_handler(youtube_handler.handle_youtube_link, lambda message: 'youtube' in message.text or 'youtu.be' in message.text)
dp.register_message_handler(playstation_handler.handle_playstation_command, commands=['playstation'])
dp.register_message_handler(myproperty_handler.handle_myproperty_command, commands=['myproperty'])
dp.register_message_handler(mycars_handler.handle_mycars_command, commands=['mycars'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)