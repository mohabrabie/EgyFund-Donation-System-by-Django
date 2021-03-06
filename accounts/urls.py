from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/projects", views.user_projects, name="accounts_projects"),
    path("profile/<int:user_id>/donations", views.user_donations, name="accounts_donations"),
    path("profile/<int:user_id>/delete", views.profile_delete, name="accounts_delete"),
    path("profile/<int:user_id>/delete/confirm", views.profile_delete_confirm, name="accounts_delete_confirm"),
    path("forbidden/", views.forbidden, name="forbidden"),
    path("activate/<uidb64>/<token>", views.verify, name='activate'),
    path("test/", views.test, name="test"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
