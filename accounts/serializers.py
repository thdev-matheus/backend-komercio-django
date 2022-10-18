from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]

        read_only_fields = [
            "date_joined",
            "is_active",
            "is_superuser",
        ]

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        model = self.Meta.model

        instance = model.objects.create_user(**validated_data)

        return instance
