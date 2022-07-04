from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, auction_listing, bid, comment

class creating_form(forms.Form):
    title = forms.CharField(label = '', max_length=64,
                            widget=forms.TextInput(attrs={
                                'class':"form-group form-control",
                                'autofocus': True,
                                'placeholder': "Title" 
                            }))

    description = forms.CharField(label = '', max_length=128, 
                                widget=forms.Textarea(attrs={
                                    'class': 'form-group form-control',
                                    'placeholder': 'Description',
                                }))

    starting_bid = forms.DecimalField(label = '', widget=forms.NumberInput(attrs = {
                                        'step': '0.01',
                                        'class': 'form-group form-control',
                                        'placeholder': 'Starting bid',
                                    }))                       
    
    image = forms.CharField(label = '', max_length=128, required = False, widget=forms.TextInput(attrs={
                                'class': 'form-group form-control',
                                'placeholder': 'URL image address',
                            }))
    
    category = forms.CharField(label = '', max_length=32, widget=forms.TextInput(attrs={
                                'class': 'form-group form-control',
                                'placeholder': 'Category e.g. Fashion, Toys, Electronics, Home, etc'
                            }))
                            

def index(request):
    return render(request, "auctions/index.html",{
        "auctions": auction_listing.objects.all(),
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

@login_required(login_url="/login")
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/profile.html",{
        'user': user
    })

@login_required(login_url="/login")
def create_listings(request):
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding)
        form = creating_form(request.POST)

        #Check data is valid (server-side)
        if form.is_valid():
            
            # Isolate data from "cleaned" version of form
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]

            seller = request.user.id

            # Insert to model
            a = auction_listing(
                seller = seller,
                title = title,
                description = description,
                starting_bid = starting_bid,
                photo = image,
                category = category
            )
            a.save()

            # redirect to Active listing
            return HttpResponseRedirect(reverse("index")
                #context announce successful creating
                )
        else:
        # Form is invalid, then re-render with the existing data
            return render(request, "auction/create_listing.html",{
                'form': form
            })
                
    return render(request, "auctions/create_listing.html",{
        'form': creating_form()
    })

def listing(request, auction_id):
    # Get auction from id
    auction = auction_listing.objects.get(pk=auction_id)

    if not auction:
        return render(request, "auctions/notfound.html")

    # Check whether this listing belong current user's watchlist
    exist = True if request.user in auction.watchers.all() else False

    # Check user is seller or not
    sellerMode = True if auction.seller == request.user else False

    # Get all comment if exist
    discussion = auction.comments.all()
    
    data = {
        'auction': auction,
        'existing': exist,
        'sellerMode': sellerMode,
        'discussion': discussion
    }
    
    # Get current bidder if auction is closed
    if not auction.active:
        data["current_bidder"] = auction.bids.get(bidding=auction.current_bid)

    return render(request,"auctions/listing.html", context=data)

@login_required(login_url="/login")
def modify_watchlist(request, auction_id):
    if request.method == "POST":

        modify = int(request.POST["watchlist"])
        auction = auction_listing.objects.get(pk=auction_id)

        # Add to watchlist
        if modify:
            auction.watchers.add(request.user)
        else:
        # Remove from watchlist
            auction.watchers.remove(request.user)

        return HttpResponseRedirect(reverse("listings", args=(auction_id,)))

    return render(request, "auctions/notfound.html")

@login_required(login_url="/login")
def make_bid(request, auction_id):
    if request.method == "POST":
        bidding = float(request.POST["bid"])

        # get current bid of listing
        auction = auction_listing.objects.get(pk=auction_id)

        # If bidding - satisfy - auction
        if satisfy(bidding, auction):
            # replace current_bid
            auction.current_bid = bidding
            auction.save()

            # add current winning bidder
            instance = bid(
                user = request.user,
                bidding = bidding,
                listing = auction
            )
            instance.save()
            # add.user.add(request.user)
            # add.listing.add(auction)
        
        return HttpResponseRedirect(reverse("listings", args=(auction_id,)))

    return render(request, "auctions/notfound.html")

def satisfy(bidding, auction):
    if (bidding > auction.starting_bid) and (auction.current_bid is None or bidding > auction.current_bid):
        return True
    else:
        return False

@login_required(login_url="/login")
def close_auction(request, auction_id):
    if request.method == "POST":
        # Turn active attribute to False
        auction = auction_listing.objects.get(pk=auction_id)
        auction.active = False
        auction.save()
        
        return HttpResponseRedirect(reverse("listings", args=(auction_id,)))

    return render(request, "auctions/notfound.html")

@login_required(login_url="/login")
def make_comment(request, auction_id):
    if request.method == "POST":
        # Get data comment from POST
        data = request.POST["comment"]
        user = request.POST["user"]

        instance = comment(
            user = User.objects.get(pk=user),
            comment = data,
            listing = auction_listing.objects.get(pk=auction_id)
        ) 
        instance.save()
        return HttpResponseRedirect(reverse("listings", args=(auction_id,)))

    return render(request, "auctions/notfound.html")
