# Проект «Доставка цветов - Flower Delivery Basic»

Проект объединяет два основных компонента:

1. **Веб-сайт на Django**  
   Позволяет пользователям регистрироваться, просматривать каталог цветов, оформлять заказы и управлять ими через удобный веб-интерфейс. Администратор имеет доступ к стандартной админке Django для управления данными.

2. **Telegram‑бот**  
   Независимое приложение, позволяющее пользователям через мессенджер оформлять заказы на доставку цветов. Бот предоставляет интерактивное меню для просмотра каталога, выбора букета, работы с корзиной и оформления заказа. После оформления заказа бот отправляет уведомление в заранее настроенный чат магазина с информацией о заказе.

---

## Используемые технологии

- **Python:** 3.11.9  
- **Django:** 5.1.5  
- **aiogram:** 3.17.0  

Другие зависимости перечислены в файле [requirements.txt](requirements.txt):

- aiofiles          24.1.0  
- aiohappyeyeballs  2.4.4  
- aiohttp           3.11.11  
- aiosignal         1.3.2  
- annotated-types   0.7.0  
- asgiref           3.8.1  
- attrs             25.1.0  
- certifi           2025.1.31  
- frozenlist        1.5.0  
- idna              3.10  
- magic-filter      1.0.12  
- multidict         6.1.0  
- pillow            11.1.0  
- pydantic          2.10.6  
- pydantic_core     2.27.2  
- sqlparse          0.5.3  
- typing_extensions 4.12.2  
- tzdata            2025.1  
- yarl              1.18.3

---

## Структура проекта

```plaintext
PFDB01/
├── .venv/                     # Виртуальное окружение (Python 3.11.9)
├── bot/                       # Телеграм‑бот (независимое приложение)
│   ├── __init__.py
│   ├── config.py              # Конфигурация бота (TOKEN, SHOP_CHAT_ID и др.)
│   ├── main.py                # Точка входа бота (настройка Django, Bot, Dispatcher, middleware, регистрация роутеров)
│   ├── handlers/              # Обработчики Telegram-сообщений и callback-запросов
│   │   ├── __init__.py        # Экспорт общего роутера (например, "from .handlers import router")
│   │   ├── handlers.py        # Основные обработчики (/start, каталог, выбор букета, добавление в корзину, оформление заказа)
│   │   ├── cart.py            # (Опционально) Обработчики для работы с корзиной
│   │   ├── catalog.py         # (Опционально) Обработчики для работы с каталогом товаров
│   │   └── order.py           # (Опционально) Обработчики для оформления заказа
│   ├── fsm/                   # Конечные автоматы (FSM) для пошаговых сценариев (при необходимости)
│   │   ├── __init__.py
│   │   └── order_fsm.py       # FSM для пошагового оформления заказа
│   └── services/              # Сервисный слой (бизнес-логика)
│       ├── __init__.py
│       ├── catalog.py         # Функции для работы с каталогом (get_flower_list, get_flower_details)
│       ├── orders.py          # Функции для работы с заказами и корзиной (add_item_to_cart, get_cart_details, create_order)
│       └── notifications.py   # Функции для отправки уведомлений в чат магазина (send_order_notification)
├── flower_delivery/           # Веб-сайт на Django
│   ├── flower_delivery/       # Основной проект Django (настройки, urls, wsgi)
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── catalog/               # Приложение каталога
│   │   ├── __init__.py
│   │   ├── admin.py           # Регистрация моделей каталога в админке
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── migrations/
│   │   └── tests/             # Тесты для приложения catalog
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       └── test_views.py
│   ├── orders/                # Приложение заказов
│   │   ├── __init__.py
│   │   ├── admin.py           # Регистрация моделей заказов в админке
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── migrations/
│   │   └── tests/             # Тесты для приложения orders
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       └── test_views.py
│   ├── users/                 # Приложение пользователей
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── migrations/
│   │   └── tests/             # Тесты для приложения users
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       └── test_views.py
│   ├── static/                # Статические файлы (CSS, JavaScript, изображения)
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── images/
│   │       └── favicon.ico
│   ├── templates/             # Шаблоны сайта
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── catalog/
│   │   │   └── flower_list.html
│   │   ├── orders/
│   │   │   ├── cart.html
│   │   │   ├── checkout.html
│   │   │   └── order_list.html
│   │   └── users/
│   │       ├── login.html
│   │       └── register.html
│   ├── media/                 # Медиафайлы (например, изображения цветов)
│   └── db.sqlite3             # База данных SQLite
├── LICENCE
├── README.md
└── requirements.txt

```bash
flower_delivery/
│── catalog/              # Приложение для управления каталогом товаров
│   ├── migrations/       # Миграции базы данных
│   ├── templates/catalog/ # HTML-шаблоны для каталога
│   ├── views.py          # Контроллеры (логика обработки запросов)
│   ├── models.py         # Определение моделей базы данных
│   ├── urls.py           # URL-маршруты для каталога
│── orders/               # Приложение для управления заказами
│   ├── templates/orders/  # Шаблоны для корзины и оформления заказа
│   ├── views.py          # Контроллеры заказов
│   ├── models.py         # Определение моделей заказов
│   ├── urls.py           # URL-маршруты для заказов
│── users/                # Приложение для работы с пользователями
│   ├── templates/users/   # Шаблоны страниц входа и регистрации
│   ├── views.py          # Контроллеры пользователей
│   ├── models.py         # Определение моделей пользователей
│   ├── urls.py           # URL-маршруты для пользователей
│── flower_delivery/      # Основные настройки проекта Django
│   ├── settings.py       # Конфигурация Django
│   ├── urls.py           # Глобальные URL-маршруты проекта
│   ├── wsgi.py           # Точка входа для WSGI-сервера
│── static/               # Статические файлы (CSS, JS, изображения)
│── templates/            # Общие HTML-шаблоны (base.html)
│── manage.py             # Управление проектом (запуск сервера, миграции и т. д.)
│── requirements.txt      # Зависимости проекта
│── README.md             # Документация проекта
```


---

## Описание проекта

### Веб-сайт

- **Регистрация и аутентификация:**  
  Приложение **users** позволяет пользователям регистрироваться и входить в систему.  
- **Каталог цветов:**  
  Приложение **catalog** предоставляет функционал просмотра списка букетов, их описания и цен. Модели каталога доступны в админке через **catalog/admin.py**.  
- **Заказы:**  
  Приложение **orders** отвечает за оформление и отслеживание заказов. Заказы можно просматривать и редактировать через админку (**orders/admin.py**).  
- **Тесты:**  
  Для каждого приложения (**catalog**, **orders**, **users**) имеется директория **tests/** с тестами моделей и представлений.

### Telegram‑бот

- **Интерактивное меню:**  
  Бот (в каталоге **bot/**) предоставляет меню для просмотра каталога, работы с корзиной и оформления заказов через Telegram.
- **Обработка заказов:**  
  Пользователь выбирает букет, добавляет его в корзину, оформляет заказ, вводя данные доставки.  
- **Уведомления:**  
  После оформления заказа бот отправляет уведомление в чат магазина с информацией о заказе (номер заказа, стоимость, дата/время доставки, адрес доставки). Функция уведомления реализована в **bot/services/notifications.py**.

---

## Требования

- **Python:** 3.11.9  
- **Django:** 5.1.5  
- **aiogram:** 3.17.0  


## 🌍 Основные URL-адреса

| URL                  | Описание                           |
|----------------------|----------------------------------|
| `/`                  | Главная страница                 |
| `/catalog/`          | Каталог цветов                   |
| `/orders/cart/`      | Корзина                          |
| `/orders/checkout/`  | Оформление заказа                |
| `/users/login/`      | Вход в систему                   |
| `/users/register/`   | Регистрация нового пользователя  |
| `/admin/`           | Панель администратора Django     |

## 📦 Установка и запуск из ветки testing

1. **Клонируйте репозиторий**:
   ```sh
   git clone https://github.com/yourusername/flower_delivery.git
   cd flower_delivery
   ```

2. **Создайте виртуальное окружение и установите зависимости**:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Для macOS/Linux
   .venv\Scripts\activate  # Для Windows
   pip install -r requirements.txt
   ```

3. **Выполните миграции базы данных**:
   ```sh
   python manage.py migrate
   ```

4. **Создайте суперпользователя**:
   ```sh
   python manage.py createsuperuser
   ```

5. **Запустите сервер разработки**:
   ```sh
   python manage.py runserver
   ```

6. **Откройте в браузере**:
   ```
   http://127.0.0.1:8000/
   ```

# 🌸 Flower Delivery и тестирование

**Flower Delivery** – это веб-приложение для заказа букетов цветов. В проекте реализован каталог товаров, корзина покупок, оформление заказа и авторизация пользователей.

## 🚀 Функциональность

- Каталог цветов с изображениями, ценами и описанием.
- Добавление товаров в корзину и управление корзиной.
- Оформление заказа.
- Авторизация и регистрация пользователей.
- Адаптивный дизайн с Bootstrap.

## 📂 Структура проекта с файлами тестирования

```bash
flower_delivery/
│── catalog/              # Приложение для управления каталогом товаров
│   ├── migrations/       # Миграции базы данных
│   ├── templates/catalog/ # HTML-шаблоны для каталога
│   ├── views.py          # Контроллеры (логика обработки запросов)
│   ├── models.py         # Определение моделей базы данных
│   ├── urls.py           # URL-маршруты для каталога
│   ├── tests/            # Тесты каталога
│       ├── test_models.py  # Тестирование моделей каталога
│       ├── test_views.py   # Тестирование вьюшек каталога
│── orders/               # Приложение для управления заказами
│   ├── templates/orders/  # Шаблоны для корзины и оформления заказа
│   ├── views.py          # Контроллеры заказов
│   ├── models.py         # Определение моделей заказов
│   ├── urls.py           # URL-маршруты для заказов
│   ├── tests/            # Тесты заказов
│       ├── test_models.py  # Тестирование моделей заказов
│       ├── test_views.py   # Тестирование вьюшек заказов
│── users/                # Приложение для работы с пользователями
│   ├── templates/users/   # Шаблоны страниц входа и регистрации
│   ├── views.py          # Контроллеры пользователей
│   ├── models.py         # Определение моделей пользователей
│   ├── urls.py           # URL-маршруты для пользователей
│   ├── tests/            # Тесты пользователей
│       ├── test_views.py   # Тестирование вьюшек авторизации и регистрации
│── flower_delivery/      # Основные настройки проекта Django
│   ├── settings.py       # Конфигурация Django
│   ├── urls.py           # Глобальные URL-маршруты проекта
│   ├── wsgi.py           # Точка входа для WSGI-сервера
│── static/               # Статические файлы (CSS, JS, изображения)
│── templates/            # Общие HTML-шаблоны (base.html)
│── manage.py             # Управление проектом (запуск сервера, миграции и т. д.)
│── requirements.txt      # Зависимости проекта
│── README.md             # Документация проекта
```

## 🧪 Тестирование

### 📌 **Что мы тестируем?**

- **Каталог (`catalog/tests/`)**
  - **Модели (`test_models.py`)** – тестирование модели `Flower`.
  - **Вьюшки (`test_views.py`)** – проверка работы каталога и детального просмотра товара.

- **Заказы (`orders/tests/`)**
  - **Модели (`test_models.py`)** – тестирование `Order`, `OrderItem`, `Cart`, `CartItem`.
  - **Вьюшки (`test_views.py`)** – тесты добавления в корзину, удаления, оформления заказа.

- **Пользователи (`users/tests/`)**
  - **Вьюшки (`test_views.py`)** – проверка регистрации, авторизации, выхода из системы.

### 📌 **Как запустить тесты?**

```

Запуск тестов для конкретного приложения:
```sh
python manage.py test catalog.tests
python manage.py test orders.tests
python manage.py test users.tests
```

Запуск тестов моделей:
```sh
python manage.py test catalog.tests.test_models
python manage.py test orders.tests.test_models
```

Запуск тестов вьюшек:
```sh
python manage.py test catalog.tests.test_views
python manage.py test orders.tests.test_views
python manage.py test users.tests.test_views
```

### ✅ **Статус тестов**
- Каталог: **Пройдено** ✅
- Заказы: **Пройдено** ✅
- Пользователи: **Пройдено** ✅


## 👨‍💻 Авторы

- [Ваше имя или команда разработчиков]
- Контакты: [ваш email или ссылка на GitHub]

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. Свободно используйте и модифицируйте его. 💡


