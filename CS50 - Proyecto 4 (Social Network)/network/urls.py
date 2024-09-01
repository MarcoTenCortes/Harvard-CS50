
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow_toggle/<int:user_id>", views.follow_toggle, name="follow_toggle"),
    path("like_toggle/<int:post_id>", views.like_toggle, name="like_toggle"),
    path("following", views.following, name="following"),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post')
]
