
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("activelisting"))
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

@login_required(login_url='/login')
def createlisting(request):
    if request.method=="POST":

        listing= Listing()
        listing.seller = request.user.username
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.category = request.POST.get('category')
        listing.starting_bid = request.POST.get('startingbid')
        listing.image_link = request.POST.get('image_link')
        listing.save()
        products = Listing.objects.all()
        return render(request, "auctions/activelisting.html", {
            "products": products
        })
    else:
        return render(request, "auctions/createlisting.html")

# view for showing the active lisitngs
@login_required(login_url='/login')
def activelisting(request):
    # list of products available
    products = Listing.objects.all()
    return render(request, "auctions/activelisting.html", {
        "products": products
    })
@login_required(login_url='/login')
def viewlisting(request, product_id):
    commentz = addcomment.objects.filter(listingid=product_id)
    product = Listing.objects.get(id=product_id)
    added = Watchlistssme.objects.filter(
            listingid=product_id, user=request.user.username)
    try:
        if request.method == "POST":
            item = Listing.objects.get(id=product_id)
            newbid= int(request.POST.get('newbid'))
            product = Listing.objects.get(id=product_id)
            if item.starting_bid >= newbid:
                return render(request, "auctions/viewlisting.html", {
                "product": product,
                "message": "Failed to add Bid. Please enter a value higher than the starting bid value and try again.",
                "msg_type": "danger",
                "comments": commentz,
                "added": added
                })
            else:
                item.starting_bid = newbid
                item.save()
                cbid = addbid()
                cbid.user = request.user.username
                cbid.amount= item.starting_bid
                cbid.listingid = product_id
                cbid.save()
                product = Listing.objects.get(id=product_id)
                return render(request, "auctions/viewlisting.html", {
                "product": product,
                "message": "Your Bid is added.",
                "msg_type": "success",
                "comments": commentz,
                "added": added
                })
        else:
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/viewlisting.html", {
            "product": product,
            "comments": commentz,
            "added": added
        })
    except ValueError:
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "message": " Falied to add Bid. Oops!  That was no valid number.  Try again...",
            "msg_type": "danger",
            "comments": commentz,
            "added": added
        })
        


@login_required(login_url='/login')
def addtowatchlist(request, product_id):
    item = Listing.objects.get(id=product_id)
    added = Watchlistssme.objects.filter(
            listingid=product_id, user=request.user.username)
    wl = Watchlistssme.objects.filter(
        listingid=product_id, user=request.user.username)
    # checking if it is already added to the watchlist
    if wl:
        wl.delete()
        product = Listing.objects.get(id=product_id)
        added = Watchlistssme.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
        })
    else:
        mewatchlist = Watchlistssme()
        mewatchlist.user = request.user.username
        mewatchlist.listingid = product_id
        mewatchlist.save()
        product = Listing.objects.get(id=product_id)
        added = Watchlistssme.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added
        })

@login_required(login_url='/login')
def comment(request, product_id):
    cmt = addcomment()
    cmt.content = request.POST.get("comment")
    comments = addcomment.objects.filter(listingid=product_id)
    product = Listing.objects.get(id=product_id)
    added = Watchlistssme.objects.filter(
        listingid=product_id, user=request.user.username)
    if request.POST["comment"] == "":
         return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": added,
        "comments": comments,
        "message": " Failed to add comment. Please type something and try again.",
        "msg_type": "danger"        
    })

    cmt.user = request.user.username
    cmt.listingid = product_id
    cmt.save()
    return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": added,
        "comments": comments
    })



@login_required(login_url='/login')
def mywatchlist(request):
    mylist = Watchlistssme.objects.filter(user=request.user.username)
    present = False
    list = []
    if mylist:
        present = True
        for product in mylist:
            product = Listing.objects.get(id=product.listingid)
            list.append(product)
    return render(request, "auctions/mywatchlist.html", {
        "product_list": list,
        "present": present

    })


@login_required(login_url='/login')
def categories(request):
    return render(request, "auctions/categories.html")
   
@login_required(login_url='/login')
def category(request, categ):
    catproducts = Listing.objects.filter(category=categ)
    empty = False
    if len(catproducts) == 0:
        empty = True
    return render(request, "auctions/category.html", {
        "categ": categ,
        "empty": empty,
        "products": catproducts
    })

@login_required(login_url='/login')
def closebid(request, product_id):
    winninguser = bidwinner()
    lists = Listing.objects.get(id=product_id)
    fetched_bids = addbid.objects.all().filter(listingid=product_id)
    bidobj= fetched_bids.last()
    winninguser.seller = request.user.username + " Item name: " + lists.title
    winninguser.winner = bidobj.user
    winninguser.listingid = product_id
    winninguser.finalbid = bidobj.amount
    winninguser.save()
    lists.delete()
    bidobj.delete()
    if Watchlistssme.objects.filter(listingid=product_id):
        watchobj = Watchlistssme.objects.filter(listingid=product_id)
        watchobj.delete()
    if addcomment.objects.filter(listingid=product_id):
        commentobj = addcomment.objects.filter(listingid=product_id)
        commentobj.delete()
    winners = bidwinner.objects.all()
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "message" : "Bid Closed",
        "msg_type" : "success",
    })



@login_required(login_url='/login')
def closedlisting(request):
    winners = bidwinner.objects.all()
    return render(request, "auctions/closedlisting.html", {
        "products": winners
    })

  
