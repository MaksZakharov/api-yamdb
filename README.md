# YaMDb API

REST API сервис для сбора отзывов пользователей на произведения (книги, фильмы, музыка).

## Описание проекта

Проект решает задачу централизованного хранения и обработки пользовательских отзывов на произведения.

Позволяет:
- хранить произведения с категоризацией (жанры, категории)
- оставлять отзывы и комментарии
- формировать рейтинг на основе пользовательских оценок
- управлять доступом через роли пользователей

## Что реализовал

- Разработал REST API на Django REST Framework
- Спроектировал модели данных:
  - произведения, жанры, категории
  - отзывы и комментарии
  - кастомная модель пользователя с ролями
- Реализовал бизнес-логику:
  - рейтинги произведений
  - вложенные ресурсы (reviews → comments)
- Настроил аутентификацию (JWT)
- Реализовал систему ролей (user, moderator, admin)
- Настроил permissions для разграничения доступа
- Реализовал фильтрацию, поиск и пагинацию
- Настроил nested routing (drf-nested-routers)
- Организовал архитектуру на ViewSets и Generic Views
- Настроил тестирование (pytest) и линтинг (flake8)

## Основные возможности

- Регистрация и аутентификация пользователей
- CRUD для произведений, категорий и жанров
- Создание отзывов и комментариев
- Система рейтингов
- Ролевая модель доступа
- Фильтрация и поиск
- Пагинация результатов

## Технологический стек

Backend: Python 3.12, Django, Django REST Framework  
Аутентификация: JWT (Simple JWT)  
База данных: SQLite (dev)  
Инструменты: django-filter, drf-nested-routers  
Тестирование: pytest, pytest-django  
Качество кода: flake8  

## Установка и запуск

```bash
git clone https://github.com/IvanP1astun/api-yamdb.git
cd api-yamdb
```

### Виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Миграции и запуск

```bash
python manage.py migrate
python manage.py runserver
```

## Примеры API

Регистрация пользователя  
POST /api/v1/auth/signup/

Получение произведения  
GET /api/v1/titles/{id}/

Обновление комментария  
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

## Планы по доработке

- Переход на PostgreSQL
- Добавление Docker и docker-compose
- Настройка CI/CD
- Добавление кэширования (Redis)
- Расширение тестового покрытия
- Деплой проекта

## Авторы

- https://github.com/IvanP1astun
- https://github.com/MaksZakharov
- https://github.com/Marakes
