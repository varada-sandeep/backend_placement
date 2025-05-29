from django.urls import path
from . import views

urlpatterns = [
    path("signin/", views.signin_view, name="signin"),
    path("signout/", views.signout_view, name="signout"),
    path("auth-status/", views.check_auth_status, name="auth_status"),
]
