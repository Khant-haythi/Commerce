from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):

    name = models.CharField(max_length=64)

    def _str_ (self):
        return self.name

class AuctionListing(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10,decimal_places=2)
    image_url = models.URLField(blank=True,null=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class Bid(models.Model):

    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    def __str__(self):

        return f"{self.created_by.username} -> {self.bid_amount}"
    
class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment= models.TextField()

class Watchlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchers")

    class Meta:

        unique_together = ("user", "listing")