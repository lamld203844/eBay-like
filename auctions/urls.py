from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create_listings", views.create_listings, name="create_listings"),

    path("listings/<int:auction_id>", views.listing, name="listings"),
    
    path("listings/<int:auction_id/watchlist/add", views.add_watchlist, name="add_watchlist"),
    path("listings/<int:auction_id/watchlist/remove", views.add_watchlist, name="add_watchlist")

]
