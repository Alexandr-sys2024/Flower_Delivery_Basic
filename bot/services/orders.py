from asgiref.sync import sync_to_async
from catalog.models import Flower
from orders.models import Cart, CartItem, Order, OrderItem
from django.utils import timezone


@sync_to_async
def add_item_to_cart(user_id: int, flower_id: int) -> None:
    try:
        flower = Flower.objects.get(id=flower_id)
    except Flower.DoesNotExist:
        raise ValueError("Букет не найден")
    cart, _ = Cart.objects.get_or_create(user_id=user_id, status="OPEN")
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        flower=flower,
        defaults={'quantity': 0, 'price': flower.price}
    )
    cart_item.quantity += 1
    cart_item.save()


@sync_to_async
def get_cart_details(user_id: int):
    cart = Cart.objects.filter(user_id=user_id, status="OPEN").first()
    if not cart:
        return None
    cart_items = CartItem.objects.select_related("flower").filter(cart=cart)
    details = []
    total_price = 0
    for item in cart_items:
        details.append({
            "flower_name": item.flower.name,
            "quantity": item.quantity,
            "total": item.price * item.quantity,
        })
        total_price += item.price * item.quantity
    return details, total_price


@sync_to_async
def create_order(user_id: int, delivery_date: str, delivery_address: str):
    cart = Cart.objects.filter(user_id=user_id, status="OPEN").first()
    if not cart:
        raise ValueError("Корзина пуста")
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user_id=user_id,
        total_price=total_price,
        status="NEW",
        # Если планируется расширение, можно добавить поля доставки:
        # delivery_date=delivery_date,
        # delivery_address=delivery_address,
        created_at=timezone.now()
    )
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            flower=item.flower,
            quantity=item.quantity,
            price=item.price
        )
    cart.status = "CHECKOUT"
    cart.save()
    return order
