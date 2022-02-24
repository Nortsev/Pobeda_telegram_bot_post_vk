from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import configparser

from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Читаем config и создаём объекта парсера
config = configparser.ConfigParser()
# читаем конфиг
config.read("config.ini")
# Выбираем из config токен
token = config["Telegram"]["token_telegram"]
# Создаем обьект в памяти для сохранения данных
storage = MemoryStorage()
# Иницилизируем бота и передаем ему токен
bot = Bot(token=token)
# Иницилизируем диспечер
dp = Dispatcher(bot, storage=storage)
