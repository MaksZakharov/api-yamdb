from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from api.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,
    SignUpView, TitleViewSet, TokenView, UserViewSet,
)


v1_router = DefaultRouter()
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'genres', GenreViewSet, basename='genre')
v1_router.register(r'titles', TitleViewSet, basename='title')
v1_router.register('users', UserViewSet, basename='user')

v1_titles_router = NestedDefaultRouter(
    v1_router, r'titles', lookup='title')
v1_titles_router.register(
    'reviews', ReviewViewSet, basename='title-reviews')

v1_reviews_titles_router = NestedDefaultRouter(
    v1_titles_router, r'reviews', lookup='review')
v1_reviews_titles_router.register(
    'comments', CommentViewSet, basename='review-comments')

api_v1_patterns = [
    path('', include(v1_router.urls)),
    path('', include(v1_titles_router.urls)),
    path('', include(v1_reviews_titles_router.urls)),
    path('', include('djoser.urls.jwt')),

    # Аутентификация
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenView.as_view(), name='token'),

    # Пользователи
    path(
        'users/',
        UserViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='users'
    ),
    path(
        'users/me/',
        UserViewSet.as_view({'get': 'me', 'patch': 'me'}),
        name='me'
    ),
    path('users/<str:username>/', UserViewSet.as_view(
        {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='user-detail'
    ),
]

urlpatterns = [
    path('v1/', include(api_v1_patterns)),
]
