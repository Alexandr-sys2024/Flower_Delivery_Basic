from aiogram import Bot
from bot.config import TOKEN, SHOP_CHAT_ID
import logging

# Создаем экземпляр бота для уведомлений (или можно использовать тот же, что и в основном файле)
bot = Bot(token=TOKEN)


async def send_order_notification(order, delivery_datetime: str, delivery_address: str):
    """
    Отправляет уведомление в чат магазина.

    Параметры:
      order: объект заказа, в котором, например, order.order_key и order.total_price.
      delivery_datetime: строка с датой и временем доставки.
      delivery_address: строка с адресом доставки.

    Вы можете дополнить уведомление другими данными (например, список заказанных букетов),
    если это необходимо.
    """
    # Формируем сообщение. Здесь можно использовать HTML-разметку.
    text = (
        f"<b>Новый заказ!</b>\n\n"
        f"<b>Заказ №:</b> {order.order_key}\n"
        f"<b>Стоимость:</b> {order.total_price} руб.\n"
        f"<b>Дата и время доставки:</b> {delivery_datetime}\n"
        f"<b>Адрес доставки:</b> {delivery_address}"
    )
    try:
        await bot.send_message(SHOP_CHAT_ID, text, parse_mode="HTML")
    except Exception as e:
        logging.error("Ошибка при отправке уведомления в магазин: %s", e)
