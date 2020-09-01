from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.categories, name="categories"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create-listing/", views.create, name="create"),
    path("auction/<int:id>/delete/", views.delete, name="delete"),
    path("auction/<int:id>/edit/", views.edit, name="edit"),
    path("categories/<int:category_id>/", views.category, name="category"),
    path("auction/<int:id>/comment/", views.new_comment, name="new_comment"),
    path("auction/<int:id>/", views.auction, name="auction")
] 
