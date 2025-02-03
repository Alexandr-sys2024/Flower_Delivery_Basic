from django.urls import path
from .views import (
    cart_view,
    add_to_cart,
    remove_from_cart,
    checkout_view
)

urlpatterns = [
    path('cart/', cart_view, name='cart_view'),
    path('add/<int:flower_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:flower_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
]