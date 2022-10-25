import ipdb
from accounts.models import Account
from django.test import TestCase


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data_seller = {
            "username": "theus",
            "password": "1234",
            "first_name": "Matheus",
            "last_name": "Vieira",
            "is_seller": True,
        }

        cls.data_common = {
            "username": "jess",
            "password": "1234",
            "first_name": "Jessica",
            "last_name": "Vieira",
            "is_seller": False,
        }

        cls.account_seller = Account.objects.create_user(**cls.data_seller)
        cls.account_common = Account.objects.create_user(**cls.data_common)

    def test_first_and_last_name_max_length(self):
        max_length_first_name = self.account_seller._meta.get_field(
            "first_name"
        ).max_length
        max_length_last_name = self.account_seller._meta.get_field(
            "last_name"
        ).max_length

        self.assertEqual(max_length_first_name, 50)
        self.assertEqual(max_length_last_name, 50)

    def test_user_is_active_true(self):

        self.assertTrue(self.account_seller.is_active)
