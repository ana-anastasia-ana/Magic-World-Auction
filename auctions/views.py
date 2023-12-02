from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Category, Listing, Watchlist, Comment, Bid
from django.contrib import messages
from django.db.models import Max
from django.core.exceptions import ValidationError




def index(request):
    categories = Category.objects.all()
    listings = Listing.objects.filter(is_active=True)

    # Default to no category filter
    selected_category_id = None

    if request.method == "POST":
        selected_category_id = request.POST.get('category')
        if selected_category_id:
            listings = listings.filter(category_id=selected_category_id)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories,
        "selected_category_id": selected_category_id,
    })

def createListing(request):
    if request.method == "POST":
        # Process the form data for creating a new listing
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category_id = request.POST["category"]

        category = Category.objects.get(id=category_id)

        # Create a new listing
        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category_id=category_id,
            creator=request.user,
        )
        listing.save()

        return redirect("index")
    else:
        # Render the form to create a new listing
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })



def viewListing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    user = request.user
    allComments = Comment.objects.filter(listing=listing)

    # Get the maximum bid for the current listing
    max_bid = Bid.objects.filter(listing=listing).aggregate(Max('amount'))['amount__max']

    # Check if the user can place a bid
    can_bid = user.is_authenticated and listing.is_active and (max_bid is None or max_bid < listing.current_bid)

    # Check if the user is the creator of the listing
    is_creator = user == listing.creator

    # Check if the user is authenticated and has a watchlist
    in_watchlist = False
    if user.is_authenticated and hasattr(user, 'watchlist'):
        in_watchlist = listing in user.watchlist.listings.all()

    # Check if the auction is closed and the user has won
    is_winner = False
    if not listing.is_active and listing.winner == user:
        is_winner = True

    return render(request, 'auctions/view_listing.html', {
        'listing': listing,
        'can_bid': can_bid,
        'in_watchlist': in_watchlist,
        'max_bid': max_bid or 0,
        'allComments': allComments,
        'user': user,
        'is_creator': is_creator,
        'is_winner': is_winner,  # Add this to the context
    })




@login_required
def place_bid(request, listing_id):
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        listing = get_object_or_404(Listing, id=listing_id)

        # Check if the auction is closed
        if not listing.is_active:
            messages.error(request, 'This auction is closed. You cannot place a bid.')
            return redirect('view_listing', listing_id=listing_id)

        # Validate the bid amount
        try:
            bid_amount = float(bid_amount)
        except ValueError:
            messages.error(request, 'Invalid bid amount.')
            return redirect('view_listing', listing_id=listing_id)

        # Check if the bid meets the criteria
        if bid_amount <= listing.current_bid or bid_amount < listing.starting_bid:
            messages.error(request, 'Invalid bid amount.')
            return redirect('view_listing', listing_id=listing_id)

        # Save the bid
        new_bid = Bid(
            bidder=request.user,
            listing=listing,
            amount=bid_amount
        )
        new_bid.save()

        # Update the current bid for the listing
        listing.current_bid = bid_amount
        listing.save()

        messages.success(request, 'Bid placed successfully.')
        # Redirect with a query parameter indicating bid success
        return HttpResponseRedirect(reverse('view_listing', args=[listing_id]) + '?bid_added=true')
    else:
        # Handle the case where the request method is not POST
        return HttpResponseRedirect(reverse('index'))

def addComment(request, listing_id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=listing_id)
    message = request.POST['newComment']

    newComment = Comment(
        user=currentUser,
        listing=listingData,
        message=message
    )

    newComment.save()

    return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))


def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # Get or create the user's watchlist
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    # Add or remove the listing from the watchlist
    if listing in user_watchlist.listings.all():
        user_watchlist.listings.remove(listing)
    else:
        user_watchlist.listings.add(listing)

    return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))

def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    watchlist = request.user.watchlist

    # Remove the listing from the watchlist
    watchlist.listings.remove(listing)

    # Redirect back to the view_listing page
    return redirect('view_listing', listing_id=listing_id)

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # Check if the user is the creator of the listing
    if request.user == listing.creator:
        # Get the highest bid for the listing
        highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()

        if highest_bid:
            # Update listing details
            listing.is_active = False
            listing.save()

            # Set the highest bidder as the winner
            winner = highest_bid.bidder
            listing.winner = winner
            listing.save()

            # Perform any additional actions you need here

            messages.success(request, 'Auction closed successfully.')
        else:
            messages.error(request, 'No bids found for the listing.')

    return HttpResponseRedirect(reverse('view_listing', args=[listing_id]))

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
