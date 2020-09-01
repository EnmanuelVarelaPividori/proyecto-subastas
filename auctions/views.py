from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Auction, Comments, Bid, Category, Watchlist
from .forms import Lcreate, PlaceNewBid, CommentForm
from django.contrib.auth.decorators import login_required

def index(request):
    new_bid = Bid.objects.order_by('new_bid').last() 
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "new_bid": new_bid,  
        "auction": auction,
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "auction": auction,
        "watchlist": watchlist,
        "watchlists": Watchlist.objects.all()
    })

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_favourite'] = Watchlist.objects.filter(user=self.request.user, article=self.object).exists()
    return context

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

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", {
        "category": category,
        "auctions": category.auctions.all()
    })

@login_required(login_url="login")
def auction(request, id=id): 
    auction = Auction.objects.get(pk=id)
    if request.method == "POST":
        form = PlaceNewBid(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = request.user
            new_bid = form.cleaned_data["new_bid"]
            comment = Bid(auction=auction, user=user, new_bid=new_bid)
            comment.save()     
    else:
        form = Lcreate()
    if request.method == "POST":
        form1 = CommentForm(request.POST or None)    
        if form1.is_valid():
            user = request.user
            body = form1.cleaned_data["body"]
            comment1 = Comments(auction=auction, user=user, body=body)
            comment1.save()      
    else:
        form1 = CommentForm()     
    return render(request, "auctions/listing.html", {
        "form": PlaceNewBid,
        "form1": CommentForm,
        "comments": auction.comments.all(),
        "auction": auction,
        "bids": auction.bids.all(),
        "category": category,
        "latest_bid": Bid.objects.order_by("-id")[0]
    })
@login_required(login_url="login")
def new_comment(request, id):
    auction = Auction.objects.get(pk=id)
    if request.method == "POST":
        form_comment = CommentForm(request.POST or None)
        if form.is_valid():
            user = request.user
            body = form.cleaned_data["body"]
            comment = Comments(auction=auction, user=user, body=body)
            comment.save()      
            return redirect('../')
    else:
        form = CommentForm()   
    return render(request, "auctions/comment.html", {
        "form": CommentForm,
        "auction": auction,
        "form_comment": CommentForm
    })
@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        form = Lcreate(request.POST or None, request.FILES or None)
        if form.is_valid():    
            user = request.user
            starting_bid = form.cleaned_data["starting_bid"] 
            description = form.cleaned_data["description"]
            name = form.cleaned_data["name"]
            img = form.cleaned_data["img"]
            category = form.cleaned_data["category"]
            listing = Auction(user=user, starting_bid=starting_bid, description=description, name=name, img=img, category=category)
            listing.save()
            return redirect('index')
    else:
        form = Lcreate()   
    return render(request, "auctions/create.html", {
        "form": form,
        "categories": Category.objects.all(),
        "form_class": Lcreate

    })

@login_required(login_url="login")
def delete(request, id):
    auction = get_object_or_404(Auction, id=id, user=request.user)
    if request.method == "POST":
        auction.delete()
        return redirect ('index')
    return render(request, "auctions/delete.html", {
        "auction": auction
    })

@login_required(login_url="login")
def edit(request, id):
    auction = get_object_or_404(Auction, id=id)
    form = Lcreate(instance=auction)
    if request.method == "POST":
        form = Lcreate(request.POST or None, request.FILES or None, instance=auction)
        if form.is_valid():
            form.save()      
            return redirect('index')
    return render(request, "auctions/create.html", {
        "form": Lcreate
    })