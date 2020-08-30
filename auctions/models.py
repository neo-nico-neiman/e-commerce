from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f'{self.username}'

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    detail_one = models.CharField(blank=True, max_length=64)
    detail_two = models.CharField(blank=True, max_length=64)
    detail_three = models.CharField(blank=True, max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=256)
    category = models.CharField(max_length=64)
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Title: {self.title} - Description: {self.description} - Current Price: {self.current_price}'
class WatchList(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watch_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_user")
    
class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Comments(models.Model):
    content = models.CharField(max_length=256)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")

