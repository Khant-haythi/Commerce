from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import AuctionListing, Category, User


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
        print(request.POST) 
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
    
