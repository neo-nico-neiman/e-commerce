from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.new_listing, name="newListing"),
    path("listing/<int:listingId>", views.listing, name="listing"),
    path("watchlist/<int:listingId>", views.watchlist, name="watchlist"),
    path("bid/<int:listingId>", views.bid, name="bid")
]
