from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.TextField()


class Listing(models.Model):
    title = models.TextField()
    description = models.TextField()
    staring_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")


class ListingBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    bid = models.DecimalField(max_digits=10, decimal_places=2)


class ListingComment():
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    comment = models.TextField()
