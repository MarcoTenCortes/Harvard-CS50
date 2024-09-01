from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class User(AbstractUser):
    pass

# Model representing a category of items
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# Model representing an auction listing
class AuctionListing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)  # Cambiado a URLField
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# Model representing a bid placed on an auction listing
class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.IntegerField()
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.bid_amount}"

# Model representing a comment on an auction listing
class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter.username} - {self.comment_text[:20]}"

# Model representing a user's watchlist
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listings = models.ManyToManyField(AuctionListing, related_name='watchlisted_by')

    def __str__(self):
        return f"{self.user.username}'s Watchlist"