from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    """Проверка, является ли пользователь автором или админом."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user
