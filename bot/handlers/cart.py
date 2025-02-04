from aiogram import Router, types
from bot.services.orders import add_item_to_cart, get_cart_details
import re

router = Router()

def escape_markdown_v2(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!<>"
    import re
    return re.sub(r"([" + re.escape(escape_chars) + r"])", r"\\\1", text)

@router.callback_query(lambda c: c.data.startswith("add_to_cart"))
async def process_add_to_cart(callback: types.CallbackQuery):
    try:
        flower_id = int(callback.data.split(":")[1])
        await add_item_to_cart(callback.from_user.id, flower_id)
        await callback.answer("✅ Букет добавлен в корзину!")
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")

@router.callback_query(lambda c: c.data == "show_cart")
async def process_show_cart(callback: types.CallbackQuery):
    result = await get_cart_details(callback.from_user.id)
    if result is None:
        await callback.message.answer("🛍️ Ваша корзина пока пуста!")
        return
    details, total_price = result
    cart_text = "🛍️ *Ваша корзина:*\n\n"
    for detail in details:
        name = escape_markdown_v2(detail["flower_name"])
        cart_text += f"🔹 *{name}* x{detail['quantity']} — {detail['total']} руб.\n"
    cart_text += f"\n💳 *Итого:* {total_price} руб."
    await callback.message.answer(cart_text, parse_mode="MarkdownV2")