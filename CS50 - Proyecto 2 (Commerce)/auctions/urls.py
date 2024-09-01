from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("create", views.create_listing, name="create_listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>/", views.category_listings, name="category_listings"),
    path("closed_auctions/", views.closed_auctions, name="closed_auctions"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

