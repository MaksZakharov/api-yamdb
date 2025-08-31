## Summary: ##
    Привет! 
_Данный проект - YaMDb, который собирает отзывы пользователей на различные произведения._ 

**Проект разработан на Django REST Framework, работает посредством API запросов.**

Представления построены на вьюсетах и дженериках. Используются дефолтные роутеры и вложенные.

**Аутентификация действует через JWT (JSON Web Token).**

_В проекте написаны разные модели, например:_
- **Произведения**,
- **Жанры** и **Категории** произведений,
- **Отзывы** и **Комментарии** к ним,
- Кастомная модель **Юзера**.

_Так же реализованы:_ 
- Права доступа (пермишены),
- Пагинация, 
- Поисковая фильтрация,
- Модель пользователя с различными ролями (от админов и модераторов до простых пользователей).

---

## Стек технологий: ##

	•	Python 3.12
	•	Django 5.1.1 — основной фреймворк
	•	Django REST framework 3.15.2 — построение API
	•	Simple JWT 5.4.0 — аутентификация по токену
	•	drf-nested-routers 0.94.2 — вложенные маршруты
	•	django-filter 25.1 — фильтрация запросов
	•	pytest / pytest-django — тестирование
	•	flake8 — линтинг кода
	•	Pillow — работа с изображениями
	•	SQLite — база данных

Полный список зависимостей см. в (requirements.txt)

---

## **_Как запустить проект:_** ##

**_Клонировать репозиторий и перейти в него в командной строке:_**

    git clone https://github.com/IvanP1astun/api-yamdb.git

    cd api-yamdb

**_Cоздать и активировать виртуальное окружение:_**

***Для macOS / Linux:***

    python3 -m venv env

    source env/bin/activate

***Для Windows:***

    python -m venv env

    env/Scripts/activate


**_Установить зависимости из файла requirements.txt:_**

    python (python3) -m pip install --upgrade pip

    pip install -r requirements.txt
    

**_Выполнить миграции:_**

    python (python3) manage.py migrate
    

**_Запустить проект:_**

    python (python3) manage.py runserver

---

## Примеры запросов и ответов: ##

### Запрос: ###

_POST_ -> `/api/v1/auth/signup/`

### Тело запроса: ###

    {
        "email": "user@example.com",
        "username": "^w\\Z"
    }

### Ответ: ###

    {
        "email": "string",
        "username": "string"
    }

### Запрос: ###

_GET_ -> `/api/v1/titles/{titles_id}/`

### Тело запроса: ###

    {
        "text": "string"
    }

### Ответ: ###

    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [...],
        "category": {
          "name": "string",
          "slug": "^-$"
        }
    }

### Запрос: ###

_PATCH_ -> `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`

### Тело запроса: ###

    {
        "text": "string"
    }

### Ответ: ###

    {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
    }

---

## Авторы проекта: ##

Невероятные и непревзойдённые (как и все) студенты Яндекс Практикума :)

- https://github.com/IvanP1astun
- https://github.com/MaksZakharov
- https://github.com/Marakes
