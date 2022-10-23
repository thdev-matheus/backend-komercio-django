from rest_framework import permissions
from rest_framework.views import Request, View

from .models import Account


class OwnerPermission(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, account: Account
    ) -> bool:
        return bool(request.user.is_authenticated and request.user == account)
