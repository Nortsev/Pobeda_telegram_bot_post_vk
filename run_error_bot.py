from aiogram.utils import executor
from bot.create_bot import dp
from post.create_date_base import SQLApi
from bot import init_error_bot


# Сюда надо передать подключение к баще данных
async def on_startup(_):
    """
    Функуия вызываемая при запуске бота
    :param _:
    :return: создает подключение к баззе данных
    """
    print("Добро пожаловать в бот постинга вк")

init_error_bot.register_hendler(dp)


# Запускаем бота с параметром skip_updates=True что бы не
# реагировал на поступившие сообщения пока был офлайн
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)