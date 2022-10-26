import ipdb
from accounts.models import Account
from django.urls import reverse
from products.models import Product
from rest_framework.test import APITestCase

from . import mocks


class ProductPermissionTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        seller1 = Account.objects.create_user(**mocks.USER_SELLER1_DATA)
        cls.product_seller1 = Product.objects.create(
            **mocks.SELLER1_PRODUCT, seller=seller1
        )

        seller2 = Account.objects.create_user(**mocks.USER_SELLER2_DATA)
        cls.product_seller2 = Product.objects.create(
            **mocks.SELLER2_PRODUCT, seller=seller2
        )

    def setUp(self) -> None:
        seller2_login = self.client.post("/api/login/", mocks.USER_SELLER2_LOGIN_DATA)

        token_seller2 = seller2_login.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_seller2}")

    def test_update_product_with_non_owner_token(self):
        response = self.client.patch(
            f"/api/products/{self.product_seller1.id}/", mocks.SELLER_PRODUCT_UPDATE
        )

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_update_product_with_owner_token(self):
        response = self.client.patch(
            f"/api/products/{self.product_seller2.id}/", mocks.SELLER_PRODUCT_UPDATE
        )
        product_of_db = Product.objects.get(id=response.data["id"])

        self.assertEqual(200, response.status_code)
        self.assertEqual("Produto Atualizado", response.data["description"])
        self.assertEqual("Produto Atualizado", product_of_db.description)
