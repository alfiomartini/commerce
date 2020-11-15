from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.forms import ModelForm
from django import forms

# Models here.


class User(AbstractUser):
    whatchlist = models.ManyToManyField(
        'Listing', blank=True, related_name='users')

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    start_price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="cat_listings")
    datetime = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_listings")  # username
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    closed = models.BooleanField(default=False)
    closed_message = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.title} (Created {self.datetime.strftime('%b. %d, %Y, %H:%M')})"

    def num_comments(self):
        return self.listing_comments.all().count()

    def comments(self):
        return self.listing_comments.all()

    # return usernames of all users that made comments for a given listing
    def users_in_comments(self):
        user_list = []
        # for each comment for a given listing
        for comment in self.comments():
            user_list.append(comment.by_user.username)
        return user_list

    def num_bids(self):
        return self.listing_bids.all().count()


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bids")
    to_listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                   related_name="listing_bids", blank=True, null=True)

    def __str__(self):
        return f"({self.id}) Bid = ${self.bid} by {self.bidder} to {self.to_listing}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=1000)
    by_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments")
    to_listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments")

    def __str__(self):
        comment = self.comment + ' to ' + \
            self.to_listing.title + ' by ' + self.by_user.username
        return comment


# Forms from models here

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'start_price', 'description', 'image']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
