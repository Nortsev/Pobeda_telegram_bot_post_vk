from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import configparser

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['/Сделать_пост']
    keyboard.add(*buttons)
    print("/Сделать_пост")
    await message.answer("Бот запушен", reply_markup=keyboard)
    await message.delete()

@dp.message_handler(commands=['Сделать_пост'])
async def post_vk(message: types.message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/Энгельс", "/Саратов"]
    exit_button = ['/Завершить']
    keyboard.add(*buttons)
    keyboard.add(*exit_button)
    print("Выберите город")
    await message.answer("Выберите город", reply_markup=keyboard)

@dp.message_handler(commands="Энгельс")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Космонавтов", callback_data="kosmonavtor"))
    keyboard.add(types.InlineKeyboardButton(text="Горького", callback_data="Gorkogo"))
    keyboard.add(types.InlineKeyboardButton(text="4 квартал", callback_data="4kvartal"))
    print("Выберите Энгельс")
    await message.answer("Выберите филиал", reply_markup=keyboard)

@dp.callback_query_handler(text="kosmonavtor")
async def send_random_value(call: types.CallbackQuery):
    print("Выбран филиал космонавтов")
    await call.message.answer("Выбран филиал космонавтов")

@dp.callback_query_handler(text="Gorkogo")
async def send_random_value(call: types.CallbackQuery):
    print("Выбран филиал горького")
    await call.message.answer("Выбран филиал горького")

@dp.callback_query_handler(text="4kvartal")
async def send_random_value(call: types.CallbackQuery):
    print("Выбран филиал 4 квартал")
    await call.message.answer("Выбран филиал 4 квартал")

@dp.message_handler(commands="Саратов")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вданный момент не добавлен функционал", callback_data="/start"))
    print("Выберан Саратов")
    await message.answer("Выберите филиал", reply_markup=keyboard)

@dp.message_handler(commands="Завершить")
async def cmd_random(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.answer("/start")

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
