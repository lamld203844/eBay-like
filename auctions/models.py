from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.IntegerField()
    photo = models.CharField(max_length=128)
    category = models.CharField(max_length=32)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - Start price: {self.starting_bid}"

class bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bid}"

class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.comment}"
