from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    start_price = models.IntegerField()
    photo = models.URLField(max_length=64)
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.title} - Price: {self.price}"

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
