import sys
import os
import django
import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN

# Настройка Django: добавляем необходимые пути и загружаем настройки
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "flower_delivery"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_delivery.settings")
django.setup()

logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер (с использованием памяти для хранения состояний)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Добавляем middleware для логирования всех входящих обновлений
@dp.update.outer_middleware
async def log_update(handler, update: types.Update, data: dict):
    try:
        update_data = update.model_dump()
    except AttributeError:
        update_data = str(update)
    logging.info(f"Получено обновление: {json.dumps(update_data, indent=2, ensure_ascii=False)}")
    return await handler(update, data)

# Импортируем роутер из обработчиков (файл bot/handlers/__init__.py должен экспортировать router)
from bot.handlers import router as handlers_router

# Регистрируем роутер в диспетчере
dp.include_router(handlers_router)

async def main():
    logging.info("Бот стартует...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())