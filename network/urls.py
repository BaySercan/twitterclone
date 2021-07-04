
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("likeUnlike/<int:post_id>", views.likeUnlike, name="likeUnlike"),
    path("newPost", views.newPost, name="newPost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/<int:page>", views.profile, name="profile"),
    path("follow/<int:profile_user_id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("following/<int:page>", views.following, name="following"),
    path("editPost/<int:post_id>", views.editPost, name="editPost"),
]
