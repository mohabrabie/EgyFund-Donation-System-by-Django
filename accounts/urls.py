from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("activate/<uidb64>/<token>", views.verify, name='activate'),
    path("test/", views.test, name="test"),
]
