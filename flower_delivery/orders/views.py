from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Flower
from .models import Cart, CartItem, Order, OrderItem


def get_user_cart(user_id):
    """
    Возвращает открытую корзину (Cart) для данного пользователя по `user_id`.
    """
    if user_id:
        cart, created = Cart.objects.get_or_create(user_id=user_id, status='OPEN')
        return cart
    return None  # Если `user_id` не передан, корзина не создаётся


def add_to_cart(request, flower_id):
    """
    Добавляет букет в корзину текущего пользователя.
    """
    if not request.user.is_authenticated:
        return redirect('login')  # Гости не могут добавлять в корзину

    cart = get_user_cart(request.user.id)  # Используем `user.id` вместо `user`
    flower = get_object_or_404(Flower, id=flower_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, flower=flower)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


def remove_from_cart(request, flower_id):
    """
    Удаляет товар (CartItem) из корзины текущего пользователя.
    """
    cart = get_user_cart(request.user.id)  # Используем `user.id`
    cart_item = CartItem.objects.filter(cart=cart, flower_id=flower_id).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart_view')


def cart_view(request):
    """
    Отображает содержимое корзины пользователя.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    cart = get_user_cart(request.user.id)  # Используем `user.id`

    if not cart:
        return redirect('catalog')  # Если корзины нет, редирект в каталог

    items = cart.items.all()
    total_price = sum(item.price * item.quantity for item in items)

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price
    }
    return render(request, 'orders/cart.html', context)


def checkout_view(request):
    """
    Оформление заказа.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    cart = get_user_cart(request.user.id)  # Используем `user.id`
    items = cart.items.all()

    if not items:
        return redirect('cart_view')

    if request.method == 'POST':
        order = Order.objects.create(
            user_id=request.user.id,  # Передаём `user_id`
            status='NEW'
        )

        total_price = 0
        for item in items:
            total_price += item.price * item.quantity
            OrderItem.objects.create(
                order=order,
                flower=item.flower,
                quantity=item.quantity,
                price=item.price
            )

        order.total_price = total_price
        order.save()

        cart.status = 'CHECKOUT'
        cart.save()

        return render(request, 'orders/order_list.html', {'order': order})

    total_price = sum(item.price * item.quantity for item in items)
    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price
    }
    return render(request, 'orders/checkout.html', context)
from django.shortcuts import render

# Create your views here.
