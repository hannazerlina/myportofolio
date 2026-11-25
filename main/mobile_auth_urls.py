from django.urls import path

from main import mobile_auth

app_name = "mobile_auth"

urlpatterns = [
    path("session/", mobile_auth.session, name="session"),
    path("login/", mobile_auth.sign_in, name="login"),
    path("register/", mobile_auth.sign_up, name="register"),
    path("logout/", mobile_auth.sign_out, name="logout"),
]
