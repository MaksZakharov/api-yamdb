import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title

from reviews.models import Review, Comment, User

DATA_DIR = os.path.join('static', 'data')


class Command(BaseCommand):
    help = (
        'Импорт данных из CSV-файлов в БД '
        '(категории, жанры, тайтлы, связи жанр-тайтл и др.)'
    )

    def handle(self, *args, **kwargs):
        self.import_categories()
        self.import_genres()
        self.import_titles()
        self.import_genre_titles()
        self.import_users()
        self.import_reviews()
        self.import_comments()
        self.stdout.write(
            self.style.SUCCESS('Данные успешно импортированы!')
        )

    def import_categories(self):
        if Category.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    'Таблица Category не пуста, импорт пропущен.'
                )
            )
            return
        path = os.path.join(DATA_DIR, 'category.csv')
        with open(path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
        self.stdout.write(self.style.SUCCESS('Категории загружены.'))

    def import_genres(self):
        if Genre.objects.exists():
            self.stdout.write(
                self.style.WARNING('Таблица Genre не пуста, импорт пропущен.')
            )
            return
        path = os.path.join(DATA_DIR, 'genre.csv')
        with open(path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
        self.stdout.write(self.style.SUCCESS('Жанры загружены.'))

    def import_titles(self):
        if Title.objects.exists():
            self.stdout.write(
                self.style.WARNING('Таблица Title не пуста, импорт пропущен.')
            )
            return
        path = os.path.join(DATA_DIR, 'titles.csv')
        with open(path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
        self.stdout.write(self.style.SUCCESS('Тайтлы загружены.'))

    def import_genre_titles(self):
        # Связи many-to-many можно добавлять всегда, если есть новые
        path = os.path.join(DATA_DIR, 'genre_title.csv')
        with open(path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                title_id = row['title_id']
                genre_id = row['genre_id']
                try:
                    title = Title.objects.get(id=title_id)
                    genre = Genre.objects.get(id=genre_id)
                    title.genre.add(genre)
                except Title.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'Нет Title с id={title_id}')
                    )
                except Genre.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'Нет Genre с id={genre_id}')
                    )
        self.stdout.write(
            self.style.SUCCESS('Связи жанров и тайтлов загружены.')
        )

    def import_users(self):
        if User.objects.exists():
            self.stdout.write(
                self.style.WARNING('Таблица User не пуста, импорт пропущен.')
            )
            return
        path = os.path.join(DATA_DIR, 'users.csv')
        with open(path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    # Добавь нужные поля!
                )
        self.stdout.write(self.style.SUCCESS('Пользователи загружены.'))

    def import_reviews(self):
        if Review.objects.exists():
            self.stdout.write(
                self.style.WARNING('Таблица Review не пуста, импорт пропущен.')
            )
            return
        path = os.path.join(DATA_DIR, 'review.csv')
        with open(path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
        self.stdout.write(self.style.SUCCESS('Отзывы загружены.'))

    def import_comments(self):
        if Comment.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    'Таблица Comment не пуста, импорт пропущен.'
                )
            )
            return
        path = os.path.join(DATA_DIR, 'comments.csv')
        with open(path, encoding='utf-8') as file:
            for row in csv.DictReader(file):
                Comment.objects.get_or_create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date'],
                )
        self.stdout.write(self.style.SUCCESS('Комментарии загружены.'))
