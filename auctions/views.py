from django import template
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import BidForm, CommentForm
from .models import AuctionListing, Category, User , Bid ,Comment , Watchlist
from datetime import datetime

def index(request):
    listings = AuctionListing.objects.filter()
    return render(request, 'auctions/index.html', {'listings': listings})


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

def create_list(request):

    categories = Category.objects.all()
    if request.method == "POST":
        #print(request.POST) 
        title = request.POST ['title']
        description = request.POST.get('description')
        starting_bid = request.POST['starting_bid']
        image_url = request.POST['image_url']
        category_id = request.POST['category']

        category = Category.objects.get(id=category_id)
        listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category
                                 ,created_by=request.user)
        listing.save()

        
        return render(request, 'auctions/createList.html')

    else:

        return render(request, 'auctions/createList.html', {'categories': categories})
    
# For Listing Page
def listing_page(request, pk):

    listing = AuctionListing.objects.get(pk=pk)

    userBid = Bid.objects.all()

    comments = Comment.objects.all()

    is_watching = False

    if request.user.is_authenticated:

        is_watching = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    return render(request, "auctions/listingPage.html", {

        "listing": listing,

        "bids": userBid,

        "comments": comments,

        "is_watching": is_watching,

    })

@login_required

def add_comment(request, listing_id):

    if request.method == 'POST':

        comment = request.POST['comment']

        usercomment = Comment(comment=comment, listing=AuctionListing.objects.get(pk=listing_id), user=request.user)

        usercomment.save()

        return redirect('listing_page', listing_id=listing_id)

    else:

        return render(request, 'auctions/listingPage.html')

@login_required

def add_to_watchlist(request, pk):

    listing = AuctionListing.objects.get(pk=pk)

    Watchlist.objects.get_or_create(user=request.user, listing=listing)

    return redirect("listing_page", pk=pk)


@login_required

def remove_from_watchlist(request, pk):

    listing = AuctionListing.objects.get(pk=pk)

    Watchlist.objects.filter(user=request.user, listing=listing).delete()

    return redirect("listing_page", pk=pk)

@login_required
def place_bid(request, pk):

    listing = AuctionListing.objects.get(pk=pk)

    if request.method == "POST":

        bid = int(request.POST["bid"])

        userbid = Bid(bid_amount=bid, listing=listing, created_by =request.user,created_at=datetime.now())  

        if bid > listing.starting_bid:

            listing.starting_bid = bid

            listing.save()
            userbid.save()
            latest_bid = Bid.objects.filter(listing=listing).latest('created_at')
            return HttpResponseRedirect(reverse("listing_page", args=[pk]))

        else:

            return render(request, "auctions/listingPage.html", {"listing": listing, "error": "Invalid bid : The bid must be at least as large as the starting bid"})

    else:

        latest_bid = Bid.objects.filter(listing=listing).latest('created_at')

        return render(request, "auctions/listingPage.html", {"listing": listing, "latest_bid": latest_bid})
    
@login_required

def close_auction(request, pk):

    listing = AuctionListing.objects.get(pk=pk)

    if listing.user == request.user:

        listing.active = False

        listing.save()

        return redirect(index)