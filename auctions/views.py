from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Category, Listing, ListingBid, ListingComment, User, WatchList
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    listings = Listing.objects.all().filter(state=True)

    return render(request, "auctions/index.html", {
            'listings': listings
    })


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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required()
def categories(request):

    if request.method == 'POST':

        name = request.POST["name"]

        cat = Category(name=name)
        cat.save()

        return HttpResponseRedirect(reverse("category"))

    else:
        categories = Category.objects.all()
        return render(request, 'auctions/categories.html', {
            "categories": categories
        })
    

@login_required()
def category(request, id):

    listings = Listing.objects.all().filter(category_id=id, state=True)
    return render(request, 'auctions/category.html', {
        "listings": listings
    })
    

@login_required()
def listing(request, id):
    if request.method == "POST":
        bid = request.POST["bid"]
        listing_bid = ListingBid.objects.get(listing_id=id, state=True)
        
        if int(bid) < listing_bid.bid :
            messages.error(request, "The bid must be greater that the current bid")

            return redirect(f"/listing/{id}")
    
        listing_bid.state =  False
        listing_bid.save()
        
        new_bid = ListingBid(user=request.user, listing=listing_bid.listing, bid=bid)
        new_bid.save()

        return redirect(f"/listing/{id}")

    else:
        listing = Listing.objects.get(id=id)
        listing_bid = ListingBid.objects.get(listing=listing, state=True)
        
        bid_count = ListingBid.objects.filter(listing_id=id).count()
        watch_list = WatchList.objects.filter(listing_id=id, user=request.user)

        comments = ListingComment.objects.filter(listing_id=id)
        return render(request, 'auctions/listing.html', {
                'listing': listing,
                'listing_bid': listing_bid,
                'bid_count': bid_count,
                'watch_list':watch_list,
                'comments': comments
        })


@login_required()
def create_listing(request):

    if request.method == 'POST':

        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        cat = request.POST["category"]

        category = Category.objects.get(id=int(cat))

        listing = Listing(title=title, description=description, image=image, user=request.user, category=category)
        listing_bid = ListingBid(user=request.user, listing=listing, bid=starting_bid)
        listing.save()
        listing_bid.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        categories = Category.objects.all()
        return render(request, 'auctions/create_listing.html', {
            'categories': categories
        })


@login_required()
def watch_list(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(id=listing_id)
        watch_list = WatchList.objects.filter(listing=listing, user=request.user) 

        if watch_list.exists():
            watch_list.delete()
            return HttpResponseRedirect(reverse("watch_list"))

        new_watch_list = WatchList(listing=listing, user=request.user)
        new_watch_list.save()
        return HttpResponseRedirect(reverse("watch_list"))
    else:
        watch_lists = WatchList.objects.all().filter(user=request.user)
        return render(request, 'auctions/watch_list.html', {
            "watch_lists": watch_lists
        })


def close_listing(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(id=listing_id)

        listing.state = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def comment(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        comment = request.POST["comment"]

        listing = Listing.objects.get(id=listing_id)
        c = ListingComment(user=request.user, comment=comment, listing=listing) 
        c.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

