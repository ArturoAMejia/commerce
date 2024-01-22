from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.TextField()


class Listing(models.Model):
    title = models.TextField()
    description = models.TextField()
    image = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    state = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ListingBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.BooleanField(default=True)


class ListingComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    comment = models.TextField()


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_watchlist')