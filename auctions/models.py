from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxLengthValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    category_list = models.CharField(max_length=64)
    img = models.ImageField(upload_to='category_image', null=True)

    def __str__(self):
        return f'{self.category_list}'

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=64)
    img = models.ImageField(upload_to='listing_image', null=True, default="/static/default_image.jpg")
    description = models.TextField(blank=True)
    starting_bid = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions", null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.id}:{self.user} has published "{self.name}", starting bid of ${self.starting_bid}: {self.category}'
    
class Comments(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    body = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['created_on']
     
    def __str__(self):
        return f"{self.id}: {self.user} commented '{self.body}' on {self.auction} "

class Bid(models.Model):
    auction =  models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    new_bid = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.user} placed a bid of '${self.new_bid}' on {self.auction} "

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'auction')

    def __str__(self):
        return f"{self.id}: {self.user} - {self.auction.name}"