from django.db import IntegrityError
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, mixins, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

import secrets


from api.permissions import (
    AuthorAdminModerOrReadOnly,
    IsAdminOrSuperuser,
    IsAdminOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    SignUpSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title, User
from api.filters import TitleFilter


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет для управления категориями произведений.

    Доступ открыт только администраторам.
    Поиск осуществляется по полю name.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет для управления жанрами произведений.

    Доступ открыт только администраторам.
    Поиск осуществляется по полю name.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления произведениями.

    Позволяет создавать, просматривать, редактировать и удалять произведения.
    В зависимости от метода запроса используется разный сериализатор:
    - GET → TitleReadSerializer
    - POST/PATCH/PUT → TitleWriteSerializer
    """

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name', 'year', 'category__slug', 'genre__slug')
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def update(self, request, *args, **kwargs):
        """Разрешаем только PATCH (частичное обновление)."""
        if request.method.lower() == 'patch':
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def generate_code():
    """Генерация кода подтверждения."""
    return secrets.token_hex(16)


class SignUpView(APIView):
    """Обработка регистрации пользователей."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        try:
            # Пытаемся найти пользователя по email или username
            user = User.objects.filter(email=email).first()
            if user:
                # Если username отличается - возвращаем ошибку
                if user.username != username:
                    raise ValidationError(
                        {'email': 'Пользователь с таким email уже существует'}
                    )
                # Если username совпадает - обновляем код
                user.confirmation_code = generate_code()
                user.save()
            else:
                # Проверяем, не занят ли username другим пользователем
                if User.objects.filter(username=username).exists():
                    raise ValidationError(
                        {'username':
                         'Пользователь с таким username уже существует'}
                    )
                # Создаем нового пользователя
                user = User.objects.create(
                    email=email,
                    username=username,
                    confirmation_code=generate_code()
                )
            # Отправляем письмо с кодом подтверждения
            send_mail(
                'Код подтверждения YaMDb',
                f'Ваш код подтверждения: {user.confirmation_code}',
                'yamdb@example.com',
                [email],
                fail_silently=False,
            )
            # Возвращаем данные пользователя вместо сообщения
            return Response(
                {'email': email, 'username': username},
                status=status.HTTP_200_OK
            )
        except IntegrityError:
            raise ValidationError(
                {'username': 'Пользователь с таким username уже существует.'}
            )


class TokenView(APIView):
    """Получение JWT-токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not hasattr(
            user,
            'confirmation_code'
        ) or not user.confirmation_code:
            return Response(
                {'confirmation_code': 'Код подтверждения не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.confirmation_code != confirmation_code:
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями (только для администраторов)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperuser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request):
        """Получение и редактирование своих данных."""
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            # Запрещаем обычным пользователям менять свою роль
            if 'role' in serializer.validated_data:
                serializer.validated_data.pop('role')
            serializer.save()
            return Response(serializer.data)
        if request.method == 'DELETE':
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BasicReviewAndCommentViewSet(viewsets.ModelViewSet):
    """Базовые настройки прав для review и comment вьюсетов."""

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorAdminModerOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class ReviewViewSet(BasicReviewAndCommentViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_pk'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentViewSet(BasicReviewAndCommentViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_pk'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=self.get_review(),
            author=self.request.user
        )
