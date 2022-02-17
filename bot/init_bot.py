from aiogram import types, Dispatcher
from bot.create_bot import dp, bot
import logging


# Инициализация лога
logging.basicConfig(level=logging.INFO)
info = []
store_engels = {
    'kosmonavtov': '🏪Космонавтов',
    'gorkogo': '🏪Горького',
    '4kvartal': '🏪4 Квартал',
}

store_saratov = {
    'Sovet': '🏪Советская',
    '50_let': '🏪50 лет октября',
    'Chernishevskogo': '🏪Чернышевского',
    'Sokolova': '🏪Соколовая',
}

cites_name = {
    'Энгельс': store_engels,
    'Саратов': store_saratov
}
categories = {
    'phone': '📱Телефоны',
    'avto': '🚘Авто',
    'instrument': '🛠Инструмент',
    'computer': '💻Компьютерная техника',
}

def  create_reply_keyboard():
    return types.ReplyKeyboardMarkup(resize_keyboard=True)

def categories_keyboard(keyboard):
    for callback, store_info in categories.items():
        add_inline_button(keyboard, store_info, callback)

def create_inline_keyboard():
    """
    Создание обьекта клавиатуры
    :return:
    """
    return types.InlineKeyboardMarkup()


def add_inline_button(keyboard, store_info, callback):
    """
    Создание шаблона клавиатуры
    :return:
    """
    keyboard.add(types.InlineKeyboardButton(text=store_info, callback_data=callback))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.message):
    """
    Стартовая функция отображает приветвие и кнопку Начать
    :return:
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['👋Начать']
    keyboard.add(*buttons)
    print("Начать")
    await message.answer("Добро пожаловать в бот постинга вк", reply_markup=keyboard)
    await message.delete()


@dp.message_handler(text=['👋Начать'])
async def post_vk(message: types.message):
    """
    Функция отображения кнопок с названием городов и кнопка завершить
    :param message: обект types.message библиотеки aiogram
    :return: при нажатии возвращает название города или завершает работу
    """
    keyboard = create_reply_keyboard()
    buttons = [f'{city}' for city in cites_name]
    exit_button = ['🔴Завершить']
    keyboard.add(*buttons)
    keyboard.add(*exit_button)
    print("Выберите город")
    await message.answer("Выберите город", reply_markup=keyboard)
    await message.delete()


@dp.message_handler(text=cites_name)
async def cmd_sity(message: types.Message):
    """
    Функция принимает название города и возврашает кнопки с названиями филиалов
    :param message: обект types.message библиотеки aiogram
    :return: Добавляет в список  info название выбранного города
    """
    info.clear()
    city = message.text
    keyboard = create_inline_keyboard()
    for callback, store_info in cites_name[city].items():
        add_inline_button(keyboard, store_info, callback)
    info.append(city)
    print(f"Выбран {city}")
    await message.answer("Выберите филиал", reply_markup=keyboard)
    await message.delete()




@dp.callback_query_handler(text=store_engels.keys())
async def smd_engels_filial_categories(call: types.CallbackQuery):
    """
    Функция запускается при выборе горада энгельса и возврашает кнопки с названиями категорий
    :param call: Объект обратного вызова библиотеки aiogram
    :return: Добавляет в список  info название выбранного филиала
    """
    print(f"Выбран филиал {store_engels[call.data]}")
    keyboard = create_inline_keyboard()
    categories_keyboard(keyboard)
    info.append(store_engels[call.data][1:])
    await call.message.answer(f"Выберите категрию филиала  {store_engels[call.data]}", reply_markup=keyboard)


@dp.callback_query_handler(text=store_saratov.keys())
async def smd_saratov_filial_categories(call: types.CallbackQuery):
    """
    Функция запускается при выборе города Саратова и возврашает кнопки с названиями категорий
    :param call: Объект обратного вызова библиотеки aiogram
    :return: Добавляет в список info название выбранного филиала
    """
    print(f"Выбран филиал {store_saratov[call.data]}")
    keyboard = create_inline_keyboard()
    categories_keyboard(keyboard)
    info.append(store_saratov[call.data][1:])
    await call.message.answer(f"Выбран филиал {store_saratov[call.data]}", reply_markup=keyboard)

@dp.callback_query_handler(text=categories.keys())
async def smd_fihish_info(call: types.CallbackQuery):
    """
    Функция запускается при выборе категории и вовращает кнопку отправить
    :param call: Объект обратного вызова библиотеки aiogram
    :return: Добавляет в лист info название выбранной категории
    """

    print(f"Выбранна категория {categories[call.data]}")
    if len(info) == 1:
        info.append(categories[call.data][1:])
    else:
        info.insert(2, categories[call.data][1:])
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_send = ['✉️Отправить']
    buttons_end = ['🔴Завершить']
    keyboard.add(*buttons_send)
    keyboard.add(*buttons_end)
    await call.message.answer(f"Выбранна категория {categories[call.data]}")
    await call.message.answer(f"Для оправки на сервер готовы данные Город '{info[0]}'\n Филиал '{info[1]}'\n Категория '{info[2]}'\n",
                              reply_markup=keyboard)

@dp.message_handler(text="🔴Завершить")
async def cmd_end(message: types.Message):
    """
    Фукция завершает общение с пользователем
    :param message: обект types.message библиотеки aiogram
    :return: Прощальное сообщение и картинку
    """
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.send_photo(chat_id=message.chat.id, photo=open('img/bye.jpeg', 'rb'))
    await message.answer("/start")

@dp.message_handler(text="✉️Отправить")
async def cmd_send(message: types.Message):
    """
    проверят длину списка info на на личие всех 3 обьектов и опраляет данные
    выводит ошибку при не достаточности данных в списке info
    :param message:
    :return:
    """
    text = f"Ваши данные будут оправленны на сервер"
    keyboard = create_reply_keyboard()
    exit_button = ['🔴Завершить']
    keyboard.add(*exit_button)
    if len(info) == 3:
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await message.answer(text=text, reply_markup=keyboard)
    else:
        await message.answer(f"Данных не достаточно попробуте заново", reply_markup=keyboard)
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
    dp.register_message_handler(post_vk, commands=['Отправить'])
