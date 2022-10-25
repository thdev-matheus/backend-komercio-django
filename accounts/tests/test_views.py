import ipdb
from django.urls import reverse
from rest_framework.test import APITestCase


class AccountRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_correct_data = {
            "username": "theus",
            "password": "1234",
            "first_name": "Matheus",
            "last_name": "Vieira",
            "is_seller": True,
        }

    def test_creation_user_with_correct_data(self):
        ...
