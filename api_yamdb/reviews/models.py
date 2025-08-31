import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator, MaxLengthValidator,
                                    MaxValueValidator, MinValueValidator)
from django.db import models
from django.utils.text import Truncator

from reviews.constants import TRUNCATE_TEXT


class Category(models.Model):
    """
    Модель категории произведений.

    Например: Книги, Фильмы, Музыка.
    """

    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        """
        Возвращает строковое представление категории,
        сокращенное до 30 символов.
        """
        return Truncator(self.name).chars(TRUNCATE_TEXT)


class Genre(models.Model):
    """
    Модель жанра произведений.

    Например: Сказка, Артхаус, Рок.
    """

    name = models.CharField(
        'Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']

    def __str__(self):
        """
        Возвращает строковое представление жанра, сокращенное до 30 символов.
        """
        return Truncator(self.name).chars(TRUNCATE_TEXT)


class Title(models.Model):
    """
    Модель произведения.

    Представляет фильм, книгу, песню и т.д.
    """

    name = models.CharField(
        'Название произведения',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        db_index=True,
        validators=[
            MaxValueValidator(
                datetime.date.today().year,
                message='Год выпуска не может быть больше текущего года.'
            )
        ]

    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['id']

    def __str__(self):
        """
        Возвращает строковое представление произведения,
        сокращенное до 30 символов.
        """
        return Truncator(self.name).chars(TRUNCATE_TEXT)


class GenreTitle(models.Model):
    """
    Промежуточная модель для связи жанров и произведений.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'
        ordering = ['id']

    def __str__(self):
        """
        Возвращает строковое представление связи (сокращенное).
        """
        return (f'{Truncator(self.title).chars(TRUNCATE_TEXT)}'
                f' — {Truncator(self.genre).chars(TRUNCATE_TEXT)}')


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username содержит недопустимые символы!'
            ),
            MaxLengthValidator(
                150,
                message='Username не длиннее 150 символов!'
            )
        ]
    )
    email = models.EmailField(
        unique=True,
        validators=[MaxLengthValidator(254)]
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER
    )
    confirmation_code = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name='Код подтверждения'
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        """
        Возвращает строковое представление пользователя,
        сокращенное до 30 символов.
        """
        return Truncator(self.username).chars(TRUNCATE_TEXT)


class Review(models.Model):
    """
    Модель отзыва.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    score = models.IntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка не может быть ниже 1'),
            MaxValueValidator(10, message='Оценка не может быть выше 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        """
        Возвращает строковое представление отзыва (сокращенное).
        """
        return f'Оценка: {self.score}, Текст: {
            Truncator(self.text).chars(TRUNCATE_TEXT)
        }'


class Comment(models.Model):
    """
    Модель комментария.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ['id']

    def __str__(self):
        """
        Возвращает строковое представление комментария (сокращенное).
        """
        return (f'Отзыв: {Truncator(self.review).chars(TRUNCATE_TEXT)}, '
                f'Комментарий: {Truncator(self.text).chars(TRUNCATE_TEXT)}')
