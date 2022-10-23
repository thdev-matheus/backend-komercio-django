from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(),
    ),
    path(
        "accounts/",
        views.AccountView.as_view(),
    ),
    path(
        "accounts/newest/<int:num>/",
        views.AccountNewestView.as_view(),
    ),
    path(
        "accounts/<str:user_id>/",
        views.AccountDetailUpdateView.as_view(),
    ),
    path(
        "accounts/<str:user_id>/management/",
        views.ActivateDeactivateAccountView.as_view(),
    ),
]
