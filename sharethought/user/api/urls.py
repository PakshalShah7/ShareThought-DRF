from django.urls import path
from knox.views import LogoutView, LogoutAllView

from .views import (
    SignupView,
    LoginView,
    ChangePasswordView,
    UserRetrieveUpdateView,
    UserListView,
    UserAccountDeactivateView,
    UserAccountActivateView,
    UserRequestListView,
)

app_name = "user_api"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="knox_logout"),
    path("logout-all/", LogoutAllView.as_view(), name="knox_logoutall"),
    path(
        "change-password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "<int:pk>/",
        UserRetrieveUpdateView.as_view(),
        name="user_retrieve_update",
    ),
    path(
        "deactivate/<int:pk>/",
        UserAccountDeactivateView.as_view(),
        name="user_deactivate",
    ),
    path(
        "activate/",
        UserAccountActivateView.as_view(),
        name="user_activate",
    ),
    path("request-list/", UserRequestListView.as_view(), name="user_request_list"),
    path("list/", UserListView.as_view(), name="user_list"),
]
