# main.py

from aiogram import Bot, Dispatcher, executor, types
from handlers import (
    avito_handler,
    youtube_handler,
    playstation_handler,
    myproperty_handler,
    mycars_handler,
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

# ID администратора для отправки уведомлений
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

# Пользователи, которым разрешено использовать бота
AUTHORIZED_USERNAMES = {"HJDmitry"}


async def on_startup(dp: Dispatcher):
    """Sends a startup notification to the administrator."""
    if ADMIN_CHAT_ID:
        await dp.bot.send_message(ADMIN_CHAT_ID, "Бот запущен")


@dp.message_handler(lambda message: (message.from_user.username or "") not in AUTHORIZED_USERNAMES)
async def handle_unauthorized_user(message: types.Message):
    """Ответ для пользователей без доступа."""
    await message.reply(
        "Здассссьте! Чтобы получить доступ, напишите администратору @HJDmitry"
    )

# Инициализация базы данных
initialize_database()

# Регистрация хендлеров
dp.register_message_handler(avito_handler.handle_avito_link, lambda message: 'avito' in message.text)
dp.register_message_handler(youtube_handler.handle_youtube_link, lambda message: 'youtube' in message.text or 'youtu.be' in message.text)
dp.register_message_handler(playstation_handler.handle_playstation_command, commands=['playstation'])
dp.register_message_handler(myproperty_handler.handle_myproperty_command, commands=['myproperty'])
dp.register_message_handler(mycars_handler.handle_mycars_command, commands=['mycars'])

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
