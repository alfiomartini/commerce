from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class User(AbstractUser):
    pass

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
    category = models.ForeignKey(Category,on_delete=models.CASCADE, 
               related_name="cat_listings")
    datetime = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings" ) # username
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        # return f"{self.title} (Created {self.datetime.strftime('%Y-%m-%d %H:%M')})"
        return f"{self.title} (Created {self.datetime.strftime('%b. %d, %Y, %H:%M')})"