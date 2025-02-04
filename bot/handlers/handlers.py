from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
import logging

# Импорт сервисных функций из вашего сервисного слоя.
from bot.services.catalog import get_flower_list, get_flower_details
from bot.services.orders import add_item_to_cart, get_cart_details, create_order
from bot.services.notifications import send_order_notification  # функция уведомления для магазина

router = Router()

# Главное меню (ReplyKeyboardMarkup)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Каталог"), KeyboardButton(text="🛒 Корзина")],
        [KeyboardButton(text="✅ Оформить заказ")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start – вывод главного меню
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот для заказа цветов. Выберите действие:",
        reply_markup=main_menu
    )

# Обработчик для кнопки "📋 Каталог" – получение каталога из базы
@router.message(lambda message: message.text == "📋 Каталог")
async def show_catalog(message: types.Message):
    flowers = await get_flower_list()  # Ожидается список словарей с ключами: 'id', 'name', 'price'
    text = "<b>Наш каталог</b>:\n\n"
    buttons = []
    for flower in flowers:
        # Здесь мы просто формируем текст кнопки без сложного экранирования, так как HTML-разметка требует меньше усилий.
        button_text = f"{flower['name']} — {flower['price']} руб."
        callback_data = f"select_flower:{flower['id']}"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

# Обработчик для выбора букета из каталога (через inline‑кнопки)
@router.callback_query(lambda callback: callback.data.startswith("select_flower:"))
async def flower_selected(callback: types.CallbackQuery):
    flower_id = int(callback.data.split(":")[1])
    flower = await get_flower_details(flower_id)  # Ожидается словарь с ключами: 'id', 'name', 'price', 'description'
    text = (
        f"<b>{flower['name']}</b>\n"
        f"💰 {flower['price']} руб.\n\n"
        f"{flower.get('description', '')}"
    )
    buttons = [
        [InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add_to_cart:{flower['id']}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    logging.info("Отправляем текст для выбранного букета:\n%s", text)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=keyboard)
    await callback.answer()

# Обработчик для добавления букета в корзину (через inline‑кнопку)
@router.callback_query(lambda callback: callback.data.startswith("add_to_cart:"))
async def add_to_cart_handler(callback: types.CallbackQuery):
    flower_id = int(callback.data.split(":")[1])
    await add_item_to_cart(callback.from_user.id, flower_id)
    buttons = [
        [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton(text="🛒 Перейти в корзину", callback_data="show_cart")],
        [InlineKeyboardButton(text="🏠 Перейти в главное меню", callback_data="main_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer("✅ Букет добавлен в корзину!\nЧто дальше?", reply_markup=keyboard)
    await callback.answer()

# Обработчик для просмотра корзины (через inline‑кнопку)
@router.callback_query(lambda callback: callback.data == "show_cart")
async def show_cart_handler(callback: types.CallbackQuery):
    result = await get_cart_details(callback.from_user.id)
    if result is None:
        await callback.message.answer("🛍️ Ваша корзина пуста!")
    else:
        details, total = result
        text = "<b>Содержимое корзины</b>:\n\n"
        for item in details:
            text += f"{item['flower_name']} x {item['quantity']} — {item['total']} руб.\n"
        text += f"\n<b>Итого:</b> {total} руб."
        await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

# Обработчик для возврата в главное меню (через inline‑кнопку)
@router.callback_query(lambda callback: callback.data == "main_menu")
async def main_menu_handler(callback: types.CallbackQuery):
    await callback.message.answer("🏠 Главное меню", reply_markup=main_menu)
    await callback.answer()

# Обработчик для оформления заказа – запрос данных доставки (через inline‑кнопку)
@router.callback_query(lambda callback: callback.data == "checkout")
async def checkout_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        "Пожалуйста, введите дату и время доставки (например, 2025-02-15 18:30) и адрес доставки через запятую."
    )
    await callback.answer()

# Обработчик для ввода данных доставки (ожидается, что сообщение содержит запятую)
@router.message(lambda message: "," in message.text)
async def process_delivery_info(message: types.Message):
    try:
        parts = message.text.split(",", 1)
        delivery_datetime = parts[0].strip()
        delivery_address = parts[1].strip()
        # Оформляем заказ через сервисный слой
        order = await create_order(message.from_user.id, delivery_datetime, delivery_address)
        # Отправляем уведомление в чат магазина
        await send_order_notification(order, delivery_datetime, delivery_address)
        await message.answer(
            f"Заказ оформлен! Ваш заказ №{order.order_key}.\nДата и время доставки: {delivery_datetime}\nАдрес доставки: {delivery_address}"
        )
    except Exception as e:
        await message.answer(f"Ошибка при оформлении заказа: {e}")
