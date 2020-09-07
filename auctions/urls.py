from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.new_listing, name="newListing"),
    path("listing/<int:listingId>", views.listing, name="listing"),
    path("bid/<int:listingId>", views.bid, name="bid"),
    path("close/<int:listingId>", views.closeListing, name="closeListing"),
    path("comments/<int:listingId>", views.comments, name="comments"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("watchList", views.watchList, name="watchList")
]
