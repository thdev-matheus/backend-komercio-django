from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.ProductView.as_view()),
    path("products/<str:product_id>/", views.ProductDetailView.as_view()),
]
