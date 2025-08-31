from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Чтение разрешено всем. Изменение — только пользователям с ролью admin.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAdmin(BasePermission):
    """
    Доступ только для пользователей с ролью admin.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAdminOrSuperuser(BasePermission):
    """
    Доступ для пользователей с ролью admin или суперпользователей.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class AuthorAdminModerOrReadOnly(BasePermission):
    """
    Разрешение: только автор, модератор,
    админ или суперюзер могут изменять объект.
    Просмотр разрешён всем.
    """

    def has_object_permission(self, request, view, obj):
        is_read_only = request.method in SAFE_METHODS
        is_author = obj.author == request.user
        user = request.user

        return (
            is_read_only or is_author or getattr(
                user,
                'is_admin',
                False
            ) or getattr(
                user,
                'is_moderator',
                False
            ) or user.is_superuser
        )
