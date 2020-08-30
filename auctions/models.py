from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner_id = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    detail_one = models.CharField(blank=True, max_length=64)
    detail_two = models.CharField(blank=True, max_length=64)
    detail_three = models.CharField(blank=True, max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=256)
    category = models.CharField(max_length=64)
    highest_bidder = models.IntegerField(default=0)

class Bids(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")

class Comments(models.Model):
    content = models.CharField(max_length=256)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")

class WatchList(models.Model):
    listing_id = models.IntegerField()