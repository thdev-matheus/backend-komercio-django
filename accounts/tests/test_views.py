import ipdb
from accounts.models import Account
from django.urls import reverse
from rest_framework.test import APITestCase

from . import mocks


class AccountRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_seller_correct_data = mocks.USER_SELLER1_DATA

        cls.user_incorrect_data = mocks.USER_INCORRECT_DATA

        cls.user_common_data = mocks.USER_COMMON_DATA

    def test_creation_user_seller_with_correct_data(self):
        response = self.client.post("/api/accounts/", self.user_seller_correct_data)

        self.assertEqual(201, response.status_code)
        self.assertNotIn("password", response.data)
        self.assertFalse(response.data["is_superuser"])
        self.assertTrue(response.data["is_seller"])
        self.assertTrue(response.data["is_active"])

    def test_creation_user_common_with_correct_data(self):
        response = self.client.post("/api/accounts/", self.user_common_data)

        self.assertEqual(201, response.status_code)
        self.assertNotIn("password", response.data)
        self.assertFalse(response.data["is_superuser"])
        self.assertFalse(response.data["is_seller"])
        self.assertTrue(response.data["is_active"])

    def test_must_be_persisted_the_data_in_the_database(self):
        self.client.post("/api/accounts/", self.user_seller_correct_data)

        self.assertEqual(Account.objects.count(), 1)

    def test_if_password_is_being_hashed(self):
        self.client.post("/api/accounts/", self.user_seller_correct_data)

        account = Account.objects.first()
        password_match = account.check_password(
            self.user_seller_correct_data["password"]
        )

        self.assertTrue(password_match)

    def test_should_not_be_possible_create_a_user_with_wrong_keys(self):
        response = self.client.post("/api/accounts/", self.user_incorrect_data)

        self.assertEqual(400, response.status_code)
        self.assertIn("is_seller", response.data)
        self.assertEqual("invalid", response.data["is_seller"][0].code)

    def test_should_not_be_possible_create_a_user_without_keys(self):
        response = self.client.post("/api/accounts/", {})
        expected_keys = {"username", "password", "first_name", "last_name"}
        response_keys = set(response.data.keys())

        self.assertEqual(400, response.status_code)
        self.assertSetEqual(expected_keys, response_keys)


class AccountReadViewTest(APITestCase):
    def setUp(self) -> None:
        self.client.post("/api/accounts/", mocks.USER_SELLER1_DATA)
        self.client.post("/api/accounts/", mocks.USER_SELLER2_DATA)
        self.client.post("/api/accounts/", mocks.USER_COMMON_DATA)

    def test_must_be_possible_list_all_users_without_passing_token(self):
        response = self.client.get("/api/accounts/")
        expected_keys = {"count", "next", "previous", "results"}
        response_keys = set(response.data.keys())

        self.assertEqual(200, response.status_code)
        self.assertSetEqual(expected_keys, response_keys)
        self.assertEqual(
            response.data["results"][0]["username"], mocks.USER_SELLER1_DATA["username"]
        )

    def test_must_be_possible_list_n_most_new_users_without_passing_token(self):
        response = self.client.get("/api/accounts/newest/5/")
        expected_keys = {"count", "next", "previous", "results"}
        response_keys = set(response.data.keys())

        self.assertEqual(200, response.status_code)
        self.assertSetEqual(expected_keys, response_keys)
        self.assertEqual(
            response.data["results"][0]["username"], mocks.USER_COMMON_DATA["username"]
        )


class AccountLoginViewTest(APITestCase):
    ...
