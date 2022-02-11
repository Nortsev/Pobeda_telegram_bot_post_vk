from aiogram.utils import executor
from bot.create_bot import dp
from post.create_date_base import SQLApi
from bot import init_bot


# Сюда надо передать подключение к баще данных
async def on_startup(_):
    print("Бот запущен")
    create_date_base = SQLApi()
    create_date_base.create_connection()

init_bot.register_hendler(dp)


# Запускаем бота с параметром skip_updates=True что бы не
# реагировал на поступившие сообщения пока был офлайн
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
