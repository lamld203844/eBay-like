from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class auction_listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listing")

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    photo = models.CharField(max_length=128, blank=True)
    category = models.CharField(max_length=32, blank=True)
    datetime = models.DateTimeField(auto_now=True)
    
    starting_bid = models.DecimalField(max_digits=32, decimal_places=2)
    current_bid = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)
    active = models.BooleanField(default=True)

    watchers = models.ManyToManyField(User, blank=True, null=True, related_name="watched_listings")

    def __str__(self):
        return f"{self.title}"

class bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bid")
    bidding = models.DecimalField(max_digits=32, decimal_places=2)
    listing = models.ForeignKey(auction_listing, on_delete=models.PROTECT, related_name="bids")
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.listing} {self.bidding}"

class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.comment}"