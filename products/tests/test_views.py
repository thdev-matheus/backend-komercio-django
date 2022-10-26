import ipdb
from accounts.models import Account
from django.urls import reverse
from products.models import Product
from rest_framework.test import APITestCase

from . import mocks


class ProductCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Account.objects.create_user(**mocks.USER_SELLER1_DATA)
        Account.objects.create_user(**mocks.USER_COMMON_DATA)

    def setUp(self) -> None:
        response_login_seller1 = self.client.post(
            "/api/login/", mocks.USER_SELLER1_LOGIN_DATA
        )
        response_login_common = self.client.post(
            "/api/login/", mocks.USER_COMMON_LOGIN_DATA
        )

        self.token_seller1 = response_login_seller1.data["token"]
        self.id_seller1 = response_login_seller1.data["user"]["id"]

        self.token_common = response_login_common.data["token"]

    def test_creation_of_product_with_a_non_seller_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_common}")
        response = self.client.post("/api/products/", mocks.SELLER1_PRODUCT)

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_creation_of_product_with_a_seller_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_seller1}")
        response = self.client.post("/api/products/", mocks.SELLER1_PRODUCT)
        expected_keys = {
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        }
        response_keys = set(response.data.keys())

        self.assertEqual(201, response.status_code)
        self.assertSetEqual(expected_keys, response_keys)
        self.assertEqual(self.id_seller1, response.data["seller"]["id"])

    def test_creation_of_product_with_a_wrong_keys(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_seller1}")
        response = self.client.post("/api/products/", mocks.SELLER1_PRODUCT_INCORRECT)

        self.assertEqual(400, response.status_code)
        self.assertIn("quantity", response.data)
        self.assertEqual("invalid", response.data["quantity"][0].code)
        ...

    def test_creation_of_product_with_a_negative_quantity_value(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_seller1}")
        response = self.client.post(
            "/api/products/", mocks.SELLER1_PRODUCT_NEGATIVE_QUANTITY
        )

        self.assertEqual(400, response.status_code)
        self.assertIn("quantity", response.data)
        self.assertEqual("min_value", response.data["quantity"][0].code)

    def test_creation_of_product_without_keys(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_seller1}")
        response = self.client.post("/api/products/", {})

        self.assertEqual(400, response.status_code)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("quantity", response.data)


class ProductReadFilterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        seller = Account.objects.create_user(**mocks.USER_SELLER1_DATA)
        [
            Product.objects.create(**mocks.SELLER1_PRODUCT, seller=seller)
            for _ in range(10)
        ]

    def test_list_all_products(self):
        response = self.client.get("/api/products/")
        expected_keys = {
            "count",
            "next",
            "previous",
            "results",
        }
        response_keys = set(response.data.keys())

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data["results"]))
        self.assertSetEqual(expected_keys, response_keys)

    def test_filter_product_by_id(self):
        product = Product.objects.first()
        response = self.client.get(f"/api/products/{product.id}/")
        expected_keys = {
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        }
        response_keys = set(response.data.keys())

        self.assertEqual(200, response.status_code)
        self.assertSetEqual(expected_keys, response_keys)

    def test_filter_product_that_does_not_exist(self):
        response = self.client.get(f"/api/products/produtoquenaoexiste/")

        self.assertEqual(404, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_found", response.data["detail"].code)
