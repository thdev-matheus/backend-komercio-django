from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.mixins import ProductSerializerByMethodMixin

from .models import Product
from .permissions import AdminSellerOrReadyOnlyPermission, OwnerOrReadyOnlyPermission
from .serializers import ProductDetailSerializer, ProductSerializer


class ProductView(ProductSerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminSellerOrReadyOnlyPermission]
    queryset = Product.objects.all()

    serializer_map = {
        "GET": ProductSerializer,
        "POST": ProductDetailSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailView(ProductSerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OwnerOrReadyOnlyPermission]
    queryset = Product.objects.all()
    lookup_url_kwarg = "product_id"

    serializer_map = {
        "GET": ProductDetailSerializer,
        "PATCH": ProductDetailSerializer,
    }
