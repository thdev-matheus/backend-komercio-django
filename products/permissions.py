from rest_framework import permissions, views

from products.models import Product


class AdminSellerOrReadyOnlyPermission(permissions.BasePermission):
    def has_permission(self, request: views.Request, view: views.View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_superuser or request.user.is_seller


class OwnerOrReadyOnlyPermission(permissions.BasePermission):
    def has_object_permission(
        self, request: views.Request, view: views.View, product: Product
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == product.seller
