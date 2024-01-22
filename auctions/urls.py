from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category, name="category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("comment", views.comment, name="comment"),
    path("create_listing", views.create_listing, name="create_listing")
]
