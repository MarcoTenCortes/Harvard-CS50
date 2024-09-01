from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


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

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import AuctionListing, Bid, Comment, Category, Watchlist
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": Category.objects.all()
    })

def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    min_bid = listing.starting_bid + 1  # Calcula el valor mínimo de la oferta

    # Determinar si el usuario ha ganado la subasta
    is_winner = False
    if not listing.is_active and listing.bids.exists():
        highest_bid = listing.bids.order_by('-bid_amount').first()
        if highest_bid and highest_bid.bidder == request.user:
            is_winner = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.comments.all(),
        "bids": listing.bids.all(),
        "watchlist": request.user.watchlist.all() if request.user.is_authenticated else None,
        "min_bid": min_bid,  # Pasa el valor calculado al contexto
        "is_winner": is_winner  # Pasa la información de si el usuario es ganador al contexto
    })



@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = Category.objects.get(pk=request.POST["category"])
        image_url = request.POST.get("image_url", "")  # Obtener la URL de la imagen
        auction_listing = AuctionListing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            category=category,
            owner=request.user,
            image_url=image_url  # Guardar la URL de la imagen
        )
        auction_listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


@login_required
def bid(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    bid_amount = int(request.POST["bid_amount"])
    if bid_amount > listing.starting_bid:
        new_bid = Bid(listing=listing, bidder=request.user, bid_amount=bid_amount)
        new_bid.save()
        listing.starting_bid = bid_amount
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": listing.comments.all(),
        "bids": listing.bids.all(),
        "watchlist": request.user.watchlist.all() if request.user.is_authenticated else None,
        "error_message": "Bid must be higher than current price."
    })

@login_required
def comment(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    comment_text = request.POST["comment"]
    new_comment = Comment(listing=listing, commenter=request.user, comment_text=comment_text)
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def watchlist(request):
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist.listings.all()
    })

@login_required
def add_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    # Obtener o crear la instancia de Watchlist del usuario
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listings.add(listing)  # Añadir la subasta a la lista de seguimiento
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def remove_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.listings.remove(listing)  # Elimina la subasta de la lista de seguimiento
    return HttpResponseRedirect(reverse("watchlist"))  # Redirige de nuevo a la watchlist

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    if listing.owner == request.user:
        listing.is_active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Vista para mostrar todas las categorías
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

# Vista para mostrar subastas activas en una categoría específica
def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

def closed_auctions(request):
    closed_listings = AuctionListing.objects.filter(is_active=False)
    return render(request, "auctions/closed_auctions.html", {
        "listings": closed_listings  # Nota: Usamos "listings" aquí para reutilizar el mismo nombre de variable en la plantilla
    })
