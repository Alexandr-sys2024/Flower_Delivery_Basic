from aiogram import Router, types
from aiogram.filters import Command
from bot.services.orders import create_order, get_cart_details
import logging

router = Router()

@router.message(Command("order"))
async def process_order(message: types.Message):
    # Для простоты формат: /order ГГГГ-ММ-ДД, Адрес доставки
    try:
        parts = message.text.split(maxsplit=1)[1].split(",")
        if len(parts) < 2:
            raise ValueError("Введите дату доставки и адрес через запятую")
        delivery_date = parts[0].strip()
        delivery_address = parts[1].strip()
    except Exception as e:
        await message.answer("Неверный формат. Используйте: /order ГГГГ-ММ-ДД, Адрес доставки")
        return
    try:
        order = await create_order(message.from_user.id, delivery_date, delivery_address)
        details, _ = await get_cart_details(message.from_user.id)
        await message.answer("✅ Ваш заказ оформлен!")
    except Exception as e:
        logging.exception("Ошибка при оформлении заказа")
        await message.answer(f"Ошибка при оформлении заказа: {e}")
