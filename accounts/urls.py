from django.urls import path

from django.contrib.auth.views import LoginView

from .views import UserRegistrationView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path(
        "login/", LoginView.as_view(template_name='accounts/user_login.html'),
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
]
