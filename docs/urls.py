from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # path("docs/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(),
        name="swagger-ui",
    ),
    path("docs/redoc/", SpectacularRedocView.as_view(), name="redoc"),
]
