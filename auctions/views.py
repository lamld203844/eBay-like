from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, auction_listing

class creating_form(forms.Form):
    title = forms.CharField(max_length=64,
                            widget=forms.TextInput(attrs={
                                'class':"form-group form-control",
                                'autofocus': True,
                                'placeholder': "Title" 
                            }))

    description = forms.CharField(max_length=128, 
                                widget=forms.Textarea(attrs={
                                    'class': 'form-group form-control',
                                    'placeholder': 'Description',
                                }))

    starting_bid = forms.DecimalField(widget=forms.NumberInput(attrs = {
                                        'step': '0.01',
                                        'class': 'form-group form-control',
                                        'placeholder': 'Starting bid',
                                    }))                       
    
    image = forms.CharField(max_length=128, required = False, widget=forms.TextInput(attrs={
                                'class': 'form-group form-control',
                                'placeholder': 'URL image address',
                            }))
    
    category = forms.CharField(max_length=32, widget=forms.TextInput(attrs={
                                'class': 'form-group form-control',
                                'placeholder': 'Category e.g. Fashion, Toys, Electronics, Home, etc'
                            }))
                            

def index(request):
    return render(request, "auctions/index.html",{
        "auctions": auction_listing.objects.all()
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
def create_listings(request):
    if request.method == "POST":
        #Insert to model
        
        # Take data from form
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        category = request.POST["category"]

        # if (data is validated):
        a = auction_listing(
            title = title,
            description = description,
            starting_bid = starting_bid,
            image = image,
            category = category
        )
        a.save()
        # else:

        # redirect to Active listing
        return HttpResponseRedirect(reverse("index")
            #context announce successful creating
            )
    # else:
            
    return render(request, "auctions/create_listing.html",{
        'form': creating_form
    })
