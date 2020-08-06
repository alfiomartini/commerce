from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.forms import ModelForm
from django import forms

# Create your models here.


class User(AbstractUser):
    whatchlist = models.ManyToManyField('Listing', blank=True, related_name='users')

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

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

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category','start_price','description', 'image']
        # widgets = {'owner': forms.HiddenInput()}
        # The following works. But I will try django crispy-forms
        # widgets = {
        #     'title':forms.TextInput(attrs = {'class': 'form-control'}),
        #     'category':forms.Select(attrs = {'class': 'form-control'}),
        #     'start_price':forms.NumberInput(attrs = {'class': 'form-control'}),
        #     'description':forms.Textarea(attrs = {'class': 'form-control'}),
        #     'image':forms.ClearableFileInput(attrs = {'class': 'form-control'})
            
        # }
