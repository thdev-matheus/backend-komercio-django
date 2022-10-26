import ipdb
from accounts.models import Account
from django.urls import reverse
from rest_framework.test import APITestCase

from . import mocks


class AccountPermissionsUpdateTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Account.objects.create_user(**mocks.USER_SELLER1_DATA)
        Account.objects.create_user(**mocks.USER_SELLER2_DATA)
        Account.objects.create_user(**mocks.USER_COMMON_DATA)

    def setUp(self) -> None:
        response_login_seller1 = self.client.post(
            "/api/login/", mocks.USER_SELLER1_LOGIN_DATA
        )
        response_login_seller2 = self.client.post(
            "/api/login/", mocks.USER_SELLER2_LOGIN_DATA
        )
        response_login_common = self.client.post(
            "/api/login/", mocks.USER_COMMON_LOGIN_DATA
        )

        self.token_seller1 = response_login_seller1.data["token"]
        self.id_seller1 = response_login_seller1.data["user"]["id"]

        self.token_seller2 = response_login_seller2.data["token"]
        self.id_seller2 = response_login_seller2.data["user"]["id"]

        self.token_common = response_login_common.data["token"]
        self.id_common = response_login_common.data["user"]["id"]

    def test_updating_data_with_owner_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_common}")
        response_patch = self.client.patch(
            f"/api/accounts/{self.id_common}/", mocks.USER_COMMON_UPDATE_DATA
        )
        expected_keys = {
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        }
        response_patch_keys = set(response_patch.data.keys())
        account = Account.objects.get(id=self.id_common)

        self.assertEqual(200, response_patch.status_code)
        self.assertSetEqual(expected_keys, response_patch_keys)
        self.assertEqual("Jessica Patched", response_patch.data["first_name"])
        self.assertEqual("Jessica Patched", account.first_name)

    def test_updating_data_with_non_owner_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_common}")
        response_patch = self.client.patch(
            f"/api/accounts/{self.id_seller1}/", mocks.USER_COMMON_UPDATE_DATA
        )

        self.assertEqual(403, response_patch.status_code)
        self.assertIn("detail", response_patch.data)

    def test_updating_data_without_token(self):
        response_patch = self.client.patch(
            f"/api/accounts/{self.id_common}/", mocks.USER_COMMON_UPDATE_DATA
        )

        self.assertEqual(401, response_patch.status_code)
        self.assertIn("detail", response_patch.data)

    def test_updating_data_with_incorrect_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_common}")
        response_patch = self.client.patch(
            f"/api/accounts/{self.id_common}/", mocks.USER_COMMON_UPDATE_INCORRECT_DATA
        )

        self.assertEqual(200, response_patch.status_code)
        self.assertTrue(response_patch.data["is_active"])

    def test_updating_a_data_that_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_common}")
        response_patch = self.client.patch(
            f"/api/accounts/contaquenaoexiste/", mocks.USER_COMMON_UPDATE_INCORRECT_DATA
        )

        self.assertEqual(404, response_patch.status_code)


class AccountPermissionsSoftDeleteTest(APITestCase):
    def setUp(self) -> None:
        self.client.post("/api/accounts/", mocks.USER_COMMON_DATA)
        Account.objects.create_superuser(**mocks.SUPERUSER_DATA)

        response_login_superuser = self.client.post(
            "/api/login/", mocks.SUPERUSER_LOGIN_DATA
        )
        response_login_common = self.client.post(
            "/api/login/", mocks.USER_COMMON_LOGIN_DATA
        )

        self.token_superuser = response_login_superuser.data["token"]

        self.token_common = response_login_common.data["token"]
        self.id_common = response_login_common.data["user"]["id"]

    def test_soft_delete_without_token(self):
        response = self.client.patch(f"/api/accounts/{self.id_common}/management/")

        self.assertEqual(401, response.status_code)
        self.assertIn("detail", response.data)

    def test_soft_delete_with_non_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_common}")
        response = self.client.patch(f"/api/accounts/{self.id_common}/management/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)

    def test_soft_delete_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser}")
        response = self.client.patch(f"/api/accounts/{self.id_common}/management/")

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.data["is_active"])

    def test_reactivate_account_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser}")
        self.client.patch(f"/api/accounts/{self.id_common}/management/")
        response = self.client.patch(f"/api/accounts/{self.id_common}/management/")

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.data["is_active"])

    def test_soft_delete_a_account_that_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_superuser}")
        response = self.client.patch(f"/api/accounts/contaquenaoexiste/management/")

        self.assertEqual(404, response.status_code)
