from aiogram import types, Dispatcher
from bot.create_bot import dp, bot
import logging
from test import test

# Инициализация лога
logging.basicConfig(level=logging.INFO)

store_engels = {
    'kosmonavtov': 'Космонавтов',
    'gorkogo': 'Горького',
    '4kvartal': '4 Квартал',
}

store_saratov = {
    'Sovet': 'Советская',
    '50_let': '50 лет октября',
    'Chernishevskogo': 'Чернышевского',
    'Sokolova': 'Соколовая',
}

cites_name = {
    'Энгельс': store_engels,
    'Саратов': store_saratov
}


def create_inline_keyboard():
    return types.InlineKeyboardMarkup()


def add_inline_button(keyboard, store_info, callback):
    keyboard.add(types.InlineKeyboardButton(text=store_info, callback_data=callback))


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
    buttons = [f'/{city}' for city in cites_name]
    exit_button = ['/Завершить']
    keyboard.add(*buttons)
    keyboard.add(*exit_button)
    print("Выберите город")
    await message.answer("Выберите город", reply_markup=keyboard)


@dp.message_handler(commands=cites_name)
async def cmd_sity(message: types.Message):
    city = message.text.replace('/', '')
    keyboard = create_inline_keyboard()
    for callback, store_info in cites_name[city].items():
        add_inline_button(keyboard, store_info, callback)
    print(f"Выбран {city}")
    await message.answer("Выберите филиал", reply_markup=keyboard)


@dp.callback_query_handler(text=store_engels.keys())
async def send_info(call: types.CallbackQuery):
    print(f"Выбран филиал {store_engels[call.data]}")
    await test(call.message)
    await call.message.answer(f"Выбран филиал {store_engels[call.data]}")


@dp.callback_query_handler(text=store_saratov.keys())
async def send_info(call: types.CallbackQuery):
    print(f"Выбран филиал {store_saratov[call.data]}")
    await test(call.message)
    await call.message.answer(f"Выбран филиал {store_saratov[call.data]}")


@dp.message_handler(commands="Завершить")
async def cmd_end(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.send_photo(chat_id=message.chat.id, photo=open('img/bye.jpeg', 'rb'))
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
