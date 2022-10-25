from accounts.models import Account
from django.test import TestCase
from products.models import Product
from products.serializers import ProductDetailSerializer


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data_seller = {
            "username": "theus",
            "password": "1234",
            "first_name": "Matheus",
            "last_name": "Vieira",
            "is_seller": True,
        }

        cls.data_product = {
            "description": "Descrição do Produto",
            "price": 99.90,
            "quantity": 10,
        }

        cls.account_seller = Account.objects.create_user(**cls.data_seller)
        cls.product = Product.objects.create(
            **cls.data_product, seller=cls.account_seller
        )

    def test_default_fields(self):
        self.assertTrue(self.product.is_active)

    def test_relation_product_user(self):
        account = Account.objects.get(id=self.account_seller.id)
        products = ProductDetailSerializer(account.products, many=True)
        product = ProductDetailSerializer(self.product)

        self.assertEqual(self.product.seller.id, account.id)
        self.assertIn(product.data, products.data)
