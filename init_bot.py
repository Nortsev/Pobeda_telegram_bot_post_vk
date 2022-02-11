from aiogram import types, Dispatcher
from create_bot import dp, bot
import logging
from test import test
from create_date_base import SQLApi

# Инициализация лога
logging.basicConfig(level=logging.INFO)


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
async def cmd_sity(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Космонавтов", callback_data="kosmonavtor"))
    keyboard.add(types.InlineKeyboardButton(text="Горького", callback_data="Gorkogo"))
    keyboard.add(types.InlineKeyboardButton(text="4 квартал", callback_data="4kvartal"))
    print("Выберите Энгельс")
    await message.answer("Выберите филиал", reply_markup=keyboard)


@dp.callback_query_handler(text="kosmonavtor")
async def send_one(call: types.CallbackQuery):
    print("Выбран филиал космонавтов")
    await test(call.message)
    await call.message.answer("Выбран филиал космонавтов")


@dp.callback_query_handler(text="Gorkogo")
async def send_two(call: types.CallbackQuery):
    print("Выбран филиал горького")
    await call.message.answer("Выбран филиал горького")


@dp.callback_query_handler(text="4kvartal")
async def send_thee(call: types.CallbackQuery):
    print("Выбран филиал 4 квартал")
    await call.message.answer("Выбран филиал 4 квартал")


@dp.message_handler(commands="Саратов")
async def cmd_sity2(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Советская", callback_data="Sovet"))
    keyboard.add(types.InlineKeyboardButton(text="50 лет октября", callback_data="50_let"))
    keyboard.add(types.InlineKeyboardButton(text="Чернышевского", callback_data="Chernishevskogo"))
    keyboard.add(types.InlineKeyboardButton(text="Соколовая", callback_data="Sokolova"))
    print("Выберан Саратов")
    await message.answer("Выберите филиал", reply_markup=keyboard)


@dp.message_handler(commands="Завершить")
async def cmd_end(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.send_photo(chat_id=message.chat.id, photo=open('maxresdefault.jpeg', 'rb'))
    await message.answer("/start")


@dp.message_handler()
async def send_message(message: types.message):
    if message.text == "hello":
        await message.answer("Hello friend")
    else:
        await message.answer("Данная команда отсутсвует")
    await message.delete()


def register_hendler(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(post_vk, commands=['Сделать_пост'])

