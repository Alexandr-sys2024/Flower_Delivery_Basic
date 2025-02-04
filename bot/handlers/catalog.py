from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот для заказа цветов. Выберите действие:")