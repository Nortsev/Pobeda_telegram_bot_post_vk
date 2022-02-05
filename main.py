from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import configparser

# Инициализация лога
logging.basicConfig(level=logging.INFO)
# Читаем config и создаём объекта парсера
config = configparser.ConfigParser()
# читаем конфиг
config.read("config.ini")
# Выбираем из config токен
token = config["Telegram"]["token_telegram"]

# Иницилизируем бота и передаем ему токен
bot = Bot(token=token)
# Иницилизируем диспечер
dp = Dispatcher(bot)


# Сюда надо передать подключение к баще данных
async def on_startup(_):
    print("Бот запущен")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.message):
    await message.answer("Бот запущен")

@dp.message_handler(commands=['post'])
async def post_vk(message: types.message):
    await message.answer("команда поста")


@dp.message_handler()
async def send_message(message: types.message):
        if message.text == "hello":
            await message.answer("Hello friend")
        else:
            await message.answer("Данная команда отсутсвует")
        await message.delete()





# Запускаем бота с параметром skip_updates=True что бы не
# реагировал на поступившие сообщения пока был офлайн
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
