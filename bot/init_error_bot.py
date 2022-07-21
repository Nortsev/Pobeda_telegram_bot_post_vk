from aiogram import types, Dispatcher
from bot.create_bot import dp



def create_reply_keyboard():
    return types.ReplyKeyboardMarkup(resize_keyboard=True)

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
    keyboard = create_reply_keyboard()
    exit_button = ['🔴Завершить']
    keyboard.add(*exit_button)
    await message.answer("Добро пожаловать в бот постинга вк", reply_markup=keyboard)
    await message.answer("🔴В связи проблемами на сайте бот временно не работает!🔴", reply_markup=keyboard)
    # await message.delete()

@dp.message_handler(text=['👋Начать'])
async def post_vk(message: types.message):
    """
    Функция отображения кнопок с названием городов и кнопка завершить
    :param message: обект types.message библиотеки aiogram
    :return: при нажатии возвращает название города или завершает работу
    """
    keyboard = create_reply_keyboard()
    exit_button = ['🔴Завершить']
    keyboard.add(*exit_button)
    await message.answer("Добро пожаловать в бот постинга вк", reply_markup=keyboard)
    await message.answer("🔴В связи проблемами на сайте бот временно не работает!🔴", reply_markup=keyboard)


@dp.message_handler(text="🔴Завершить")
async def cmd_end(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['👋Начать']
    keyboard.add(*buttons)
    await message.answer("Введется работа по востановлению работоспособности!", reply_markup=keyboard)



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
