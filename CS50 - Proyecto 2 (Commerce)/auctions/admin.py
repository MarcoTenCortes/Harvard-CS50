from django.contrib import admin

# Register your models here.
from .models import AuctionListing, Category, Bid, Comment, Watchlist

admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
