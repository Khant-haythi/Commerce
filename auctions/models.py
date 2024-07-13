from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):

    name = models.CharField(max_length=64)

    def __str__ (self):
        return self.name

class AuctionListing(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10,decimal_places=2)
    image_url = models.URLField(blank=True,null=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name= "owner")
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="winner")

    def __str__(self):

        return f"{self.title} on {self.category.name}" 
    


class Bid(models.Model):

    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def __str__(self):

        return f"{self.created_by.username} bid {self.bid_amount} on {self.listing.title}"
    
class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    comment= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchers")

    class Meta:

        unique_together = ("user", "listing")