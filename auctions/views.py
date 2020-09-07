from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import choices
from .models import User, Listing, WatchList, Bids, Comments
from django import forms

class NewListingForm(forms.Form):
    categoryChoices = [
        ('camping', 'Camping'),
        ('electronics', 'Electronics'),
        ('food', 'Food'),
        ('furniture', 'Furniture'),
        ('garden', 'Garden'),
        ('others', 'Others'),
        ('pets', 'Pets'),
        ('sport', 'Sport')
    ] 
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=64)
    image_url = forms.URLField(max_length=1000, required=False)
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.CharField(max_length=64, widget=forms.Select(choices=categoryChoices, attrs={ 'style': 'margin-bottom: 20px; padding: 5px'}))

class NewCommentForm(forms.Form):
    content = forms.CharField(
        widget = forms.TextInput(
            attrs= {
                'placeholder': 'Add your comment'
            }
        ),
        label=''
    )
#Global comment form
comment = NewCommentForm()

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
    form = NewListingForm()
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            imagePlaceHolder = [
                'https://images.unsplash.com/photo-1576158114131-f211996e9137?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1576158113840-43db9ff3ef09?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1576158113928-4c240eaaf360?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1573490647684-928a2454f861?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1578589302979-24448e95ef4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1576158674803-9c3b014d2c11?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1578589318433-39b5de440c3f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1579158951952-94218e428df6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1579818277076-1abc45c9471f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
                'https://images.unsplash.com/photo-1573490647695-2892d0bf89e7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60',
            ]
            # If the user does not provide an image, then include a random image
            imageURL = choices(imagePlaceHolder)[0] if not len(request.POST['image_url']) else request.POST['image_url']
            listing = Listing(
                user = User.objects.get(pk=request.user.id),
                title = request.POST['title'],
                description = request.POST['description'],
                image_url = imageURL,
                starting_bid = request.POST['starting_bid'],
                category = request.POST['category']
            )
            listing.save()
            return render(request, "auctions/listing_page.html", {
                'listing': listing,
                'comments': listing.comment_listing.all()
            })
        else:
            return render(request, "auctions/create_listing.html", {
        'form': form
    })
    return render(request, "auctions/create_listing.html", {
        'form': form
    })

def listing(request, listingId):
    is_watchList = False
    listing = Listing.objects.get( pk=listingId )
    if request.user.is_authenticated and request.user.watchList:
        watchListForUser = request.user.watchList.all()
        for watchList in watchListForUser:
            if watchList.listing.id == listing.id:
                is_watchList = True
    if request.method == 'POST':
        try:
            addToWatchList = request.POST['watchList']
            user = request.user
            if addToWatchList == '1':
                watchList = WatchList(listing=listing, user=User.objects.get(pk=user.id))
                watchList.save()
                user.watchList.add(watchList)
                is_watchList = True
            else:
                watchList = WatchList.objects.filter(listing=listing, user=User.objects.get(pk=request.user.id))
                watchList.delete()
                is_watchList = False            
        except Exception as e:
            print( e )
        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'commentForm': comment,
        'comments': listing.comment_listing.all(),
        'watchList': is_watchList
    })
    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'commentForm': comment,
        'comments': listing.comment_listing.all(),
        'watchList': is_watchList
    })

def watchList(request):
    
    try:
        watchList = request.user.watchList.all()
    except:
        watchList = None
    return render(request, "auctions/watchList.html", {
        'watchList': watchList
    })

def bid(request, listingId):
    listing = Listing.objects.get(pk=listingId)
    bid = float(request.POST['bid'])
    if bid <= listing.current_price or bid < listing.starting_bid:
        minimunBid = (listing.current_price + 1) if listing.starting_bid < listing.current_price else listing.starting_bid
        return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'watch': True,
        'message': f'Your bid must be at least {minimunBid}',
        'commentForm': comment,
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
        'comments': listing.comment_listing.all(),
        'commentForm': comment,
        })

def closeListing(request, listingId):
    listing = Listing.objects.get(pk=listingId)
    listing.is_active = False
    listing.save()
    return render(request, "auctions/listing_page.html", {
        'listing': listing,
        'comments': listing.comment_listing.all(),
        'commentForm': comment,
        })

def comments(request, listingId):
    listing = Listing.objects.get(pk=listingId)
    form = NewCommentForm(request.POST)
    if form.is_valid():

        newComment = Comments(
            content = request.POST['content'],
            listing = listing,
            user = User.objects.get(pk=request.user.id)
        )
        newComment.save()
        return render(request, "auctions/listing_page.html", {
            'listing': listing,
            'comments': listing.comment_listing.all(),
            'commentForm': comment,
            })
    else:
        return render(request, "auctions/listing_page.html", {
            'listing': listing,
            'comments': listing.comment_listing.all(),
            'commentForm': comment,
            })

def categories(request):
    categories = Listing.objects.filter(category__isnull=False).values('category').distinct()
    return render(request, "auctions/categories.html", {
        'categories': categories
    })

def category(request, category):
    listings = Listing.objects.filter(category=str(category))
    return render(request, "auctions/category.html", {
        'listings': listings
    })
