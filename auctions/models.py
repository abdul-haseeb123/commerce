import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    
    def __str__(self) -> str:
        return self.username


class Listing(models.Model):
    CATEGORY_CHOICES = (
        ("Fashion", "Fashion"),
        ("Electronics", "Electronics"),
        ("Home & Garden", "Home & Garden"),
        ("Toy & Games", "Toy & Games"),
        ("Collectibles", "Collectibles"),
        ("Sports & Outdoors", "Sports & Outdoors"),
        ("Books & Magazines", "Books & Magazines"),
        ("Automotives", "Automotives"),
        ("Music & Entertainment", "Music & Entertainment"),
        ("Art & Crafts", "Health & Beauty"),
        ("Food & Beverages", "Food & Beverages"),
        ("Pets", "Pets"),
        ("Other", "Other")
    )


    owner = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=80, choices=CATEGORY_CHOICES, default='Other')

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now
    
    def __str__(self) -> str:
        return self.name
    

class Bid(models.Model):
    listing = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)
    bid_date = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.listing.name} {self.bid_amount}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    commentor = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    comment_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.text
     
