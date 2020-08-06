from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, ListingForm, CategoryForm

# Create your views here.

def index(request):
    listings = Listing.objects.all()
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {'listings':listings,
          'counter':request.user.whatchlist.all().count()})
    else:
        return render(request, "auctions/index.html", {'listings':listings})


@login_required(login_url='login')
def list_detail(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    whatchlist = user.whatchlist.all()
    if listing in whatchlist:
        whatched = True 
    else:
        whatched = False
    # print(whatchlist)
    return render(request, "auctions/listing.html", 
        {'listing':listing, 'whatched':whatched, 
         'counter':request.user.whatchlist.all().count()})

@login_required(login_url='login')
def whatchlist_add(request, listing_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    listing = Listing.objects.get(id=listing_id)
    user.whatchlist.add(listing)
    return redirect('whatchlist')
    
@login_required(login_url='login')
def whatchlist_del(request, listing_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    listing = Listing.objects.get(id=listing_id)
    user.whatchlist.remove(listing)
    return redirect('whatchlist')
    


@login_required(login_url='login')
def whatchlist(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    whatchlist = user.whatchlist.all()
    return render(request, 'auctions/whatchlist.html', {'whatchlist':whatchlist, 
       'counter':request.user.whatchlist.all().count()})


@login_required(login_url='login')
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            # print(title)
            start_price = form.cleaned_data['start_price']
            # print(start_price)
            category = form.cleaned_data['category']
            # print(category)
            description = form.cleaned_data['description']
            # print(description)
            image = form.cleaned_data['image']
            # print(image)
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            Listing.objects.create(title=title, start_price=start_price, 
                category=category, description=description, image=image,
                owner=user)
            return redirect('index')
        else:
            return render(request, 'auctions/create.html', 
              {'form':form, 'counter':request.user.whatchlist.all().count()})
    else:
        form = ListingForm()
        return render(request, 'auctions/create.html', 
        {'form':form, 'counter':request.user.whatchlist.all().count()})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        # https://stackoverflow.com/questions/29588808/django-how-to-check-if-username-already-exists
        if User.objects.filter(username=username).exists():
            return render(request, "auctions/register.html", {
                "message": "Username already taken."})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            return redirect('login')
        # login(request, user)
        # return redirect('index')
            
    else:
        return render(request, "auctions/register.html")
