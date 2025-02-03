from django.urls import path
from .views import flower_list, flower_detail

urlpatterns = [
    # Список букетов
    path('', flower_list, name='flower_list'),

    # Детальная страница (опционально)
    path('<int:flower_id>/', flower_detail, name='flower_detail'),
]