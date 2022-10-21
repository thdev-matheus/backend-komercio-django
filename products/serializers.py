from dataclasses import field

from accounts.serializers import AccountSerializer
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "seller",
            "is_active",
        ]
