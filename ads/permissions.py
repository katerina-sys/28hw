from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwnerSelection(BasePermission):
    message = "Вы не являетесь владельцем данной подборки!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsOwnerAdOrStaff(BasePermission):
    message = "Вы не являетесь владельцем объявления или админом!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True
        return False
