from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, WatchList, Bids, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def new_listing(request):
    if request.method == 'POST':
        listing = Listing(
            user = User.objects.get(pk=request.user.id),
            title = request.POST['title'],
            description = request.POST['description'],
            image_url = request.POST['image_url'],
            starting_bid = request.POST['starting_bid'],
            category = request.POST['category']
        )
        listing.save()
        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'comments': listing.comment_listing.all()
    })
    return render(request, "auctions/create_listing.html")

def listing(request, listingId):
    is_watchList = False
    listing = Listing.objects.get( pk=listingId )
    try:
        watchList = WatchList(listing=listing, user=User.objects.get(pk=request.user.id))
        is_watchList = True
    except Exception as e:
        print('ostro')
        is_watchList = False
    if request.method == 'POST':
        try:
            is_watchList = request.POST['watchList']
            if is_watchList == 'add':
                watchList = WatchList(listing=listing, user=User.objects.get(pk=request.user.id))
                watchList.save()
                is_watchList = True
            else:
                watchList = WatchList.objects.get(listing=listing, user=User.objects.get(pk=request.user.id))
                watchList.delete()
            
        except Exception as e:
            print( e )
            watchList = WatchList.objects.get(listing=listing, user=User.objects.get(pk=request.user.id))
            is_watchList = True if watchList else False

        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'comments': listing.comment_listing.all(),
        'watch': is_watchList
    })
    print( 555, is_watchList)
    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'comments': listing.comment_listing.all(),
        'watch': is_watchList
    })

def watchlist( request, listingId):
    is_watchlist = False
    try:
        watchList = WatchList.objects.get(listing_id=listingId, user_id=request.user.id)
        if watchList is not None:
            is_watchlist = True
    except:
        is_watchlist = False

    listing = Listing.objects.get( pk=listingId )
    if is_watchlist:
        watchlists.delete()
        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'watch': False,
        'comments': listing.comment_listing.all()
        })
    else:  
        watchList = WatchList(listing_id=listingId, user_id=request.user.id)
        watchList.save()
        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'watch': True,
        'comments': listing.comment_listing.all()
        } )

def bid(request, listingId):
    listing = Listing.objects.get(pk=listingId)
    bid = float(request.POST['bid'])
    if bid <= listing.current_price or bid < listing.starting_bid:
        minimunBid = (listing.current_price + 1) if listing.starting_bid < listing.current_price else listing.starting_bid
        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'watch': True,
        'message': f'Your bid must be at least {minimunBid}'
        })
    else:
        listing.current_price=request.POST['bid']
        listing.highest_bidder = User.objects.get(pk=request.user.id)
        listing.save()
        bid = Bids(listing=listing, user=User.objects.get(pk=request.user.id), amount=request.POST['bid'])
        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'watch': True,
        'message': 'Your bid as been accepted!',
        'comments': listing.comment_listing.all()
        })

def closeListing(request, listingId):
    listing = Listing.objects.get(pk=listingId)
    listing.is_active = False
    listing.save()
    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'comments': listing.comment_listing.all()
        })
def comments(request, listingId):
    listing = Listing.objects.get(pk=listingId)
    comment = Comments(
        content = request.POST['content'],
        listing = listing,
        user = User.objects.get(pk=request.user.id)
    )
    comment.save()
    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'comments': listing.comment_listing.all()
        })
def categories(request):
    categories = Listing.objects.filter(category__isnull=False).values('category')
    return render(request, "auctions/categories.html", {
        'categories': categories
    })

def category(request, category):
    x = f' my {category}'
    print(type(category))
    listings = Listing.objects.filter(category=str(category))
    print(999, listings)
    return render(request, "auctions/category.html", {
        'listings': listings
    })
