from django.urls import path

from .views import UserRegistrationView, LogoutView, UserLoginView, profile_view, profile_update_view


app_name = 'accounts'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView.as_view(),
        name="user_registration"
    ),
    path(
        "profile/", profile_view, name="profile"
    ),
    path(
        "profile_update/", profile_update_view, name="profile_update"
    )
]
