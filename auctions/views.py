from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, ListingForm
from .models import CategoryForm, CommentForm, BidForm
from .models import Comment, Bid


# Create your views here.

def index(request):
    listings = Listing.objects.all()
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {'listings': listings,
                                                       'counter': request.user.whatchlist.all().count()})
    else:
        return render(request, "auctions/index.html", {'listings': listings})


@login_required(login_url='login')
def readme(request):
    return render(request, 'auctions/readme.html', {})


@login_required(login_url='login')
def list_detail(request, listing_id):
    user_id = request.user.id
    username = request.user.username
    user = User.objects.get(id=user_id)
    listing = Listing.objects.get(id=listing_id)
    if user == listing.owner:
        can_close = True
    else:
        can_close = False
    closed = listing.closed
    if closed:
        closed_message = listing.closed_message
    else:
        closed_message = None

    bids = listing.listing_bids.all()
    bids_list = list(bids.order_by('-bid'))
    num_bids = bids.count()

    if num_bids > 0:
        highest_bid = bids_list[0].bid
        highest_bidder = bids_list[0].bidder.username
    else:
        highest_bid = 0
        highest_bidder = None

    can_place_bid = request.user != listing.owner

    whatchlist = user.whatchlist.all()
    if username not in listing.users_in_comments():
        can_comment = True
    else:
        can_comment = False
    if listing in whatchlist:
        whatched = True
    else:
        whatched = False
    return render(request, "auctions/listing.html",
                  {'listing': listing, 'whatched': whatched,
                   'counter': request.user.whatchlist.all().count(),
                   'can_comment': can_comment,
                   'form': CommentForm(),
                   'bid_form': BidForm(),
                   'highest_bid': highest_bid,
                   'num_bids': num_bids,
                   'highest_bidder': highest_bidder,
                   'closed': closed,
                   'can_close': can_close,
                   'closed_message': closed_message,
                   'can_place_bid': can_place_bid})


@login_required(login_url='login')
def whatchlist(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    whatchlist = user.whatchlist.all()
    return render(request, 'auctions/whatchlist.html', {'whatchlist': whatchlist,
                                                        'counter': request.user.whatchlist.all().count()})


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
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            start_price = form.cleaned_data['start_price']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            Listing.objects.create(title=title, start_price=start_price,
                                   category=category, description=description, image=image,
                                   owner=user)
            return redirect('index')
        else:
            return render(request, 'auctions/create.html',
                          {'form': form, 'counter': request.user.whatchlist.all().count()})
    else:
        form = ListingForm()
        return render(request, 'auctions/create.html',
                      {'form': form,
                       'counter': request.user.whatchlist.all().count()})


@login_required(login_url='login')
def add_comment(request, listing_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            comment = form.cleaned_data['comment']
            listing = Listing.objects.get(id=listing_id)
            Comment.objects.create(
                comment=comment, to_listing=listing, by_user=user)
            return redirect('index')
        else:
            return redirect('listing', listing_id=listing_id)
    else:
        return redirect('listing', listing_id=listing_id)


@login_required(login_url='login')
def place_bid(request, listing_id):
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(id=listing_id)
            start_price = listing.start_price
            # bids here are full objects
            bids = list(listing.listing_bids.all().order_by('-bid'))
            if bids:
                highest_bid = bids[0].bid
            else:
                highest_bid = 0
            placed_bid = form.cleaned_data['bid']
            if placed_bid < start_price:
                message = f'Placed bid is smaller than start price (${start_price})'
                return render(request, 'auctions/error.html', {'message': message})
            if placed_bid <= highest_bid:
                message = f'Placed bid must be bigger than current bid (${highest_bid})'
                return render(request, 'auctions/error.html', {'message': message})
            # update bid object
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            print('before accessing Bid.objects')
            try:
                bid_obj = Bid.objects.get(to_listing=listing, bidder=user)
            except Bid.DoesNotExist:
                # new bid
                Bid.objects.create(
                    bid=placed_bid, bidder=user, to_listing=listing)
            else:  # udpate bid
                bid_obj.bid = placed_bid
                bid_obj.bidder = user
                # update current user bid as the highest bid
                bid_obj.save()
            return redirect('listing', listing_id=listing_id)
        else:
            return redirect('listing', listing_id=listing_id)


@login_required(login_url='login')
def close_auction(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    closed = True
    listing.closed = closed

    bids = listing.listing_bids.all()
    bids_list = list(bids.order_by('-bid'))
    num_bids = bids.count()

    if num_bids > 0:
        highest_bid = bids_list[0].bid
        highest_bidder = bids_list[0].bidder
        winner = highest_bidder
    else:
        highest_bid = 0
        highest_bidder = None
        winner = None
    if num_bids > 0 and request.user == winner:
        closed_message = f'You are the winner of this auction with a bid of ${highest_bid}'
    if num_bids > 0 and request.user != winner:
        closed_message = f"This auction was won by {highest_bidder.username} with a bid of ${highest_bid}"
    if num_bids == 0:
        closed_message: 'Auction closed by owner without any bids being placed'

    listing.closed_message = closed_message
    listing.save()

    return redirect('listing', listing_id=listing_id)


def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories,
                                                        'counter': request.user.whatchlist.all().count()})


def category_listings(request, category_id):
    # print('Hello Category Listings')
    category = Category.objects.get(id=category_id)
    listings = category.cat_listings.all()
    return render(request, 'auctions/cat_listings.html', {'category': category,
                                                          'listings': listings})


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
