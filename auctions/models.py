from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime



class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    pass

# Define the Category model for different listing categories
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# Define the Listing model representing each auction listing
class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name='listingWatchlist')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return f"{self.title}"
    
    def display_details(self):
        return f"{self.title} - {self.category.name} - Current Bid: {self.current_bid}"

    # Customize the display of the method in the admin
    display_details.short_description = 'Listing Details'
    display_details.admin_order_field = 'current_bid'
    display_details.boolean = 'is_active'


# Add Bid model to track bids for each listing
class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Define the Watchlist model
class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlists")


    def __str__(self):
        return f"{self.user.username}"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='userComment')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listingComment')
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} comment on {self.listing}"

