import os
import django

# Configuración para que el script se ejecute de forma independiente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commerce.settings")
django.setup()

from auctions.models import User, Category, AuctionListing, Bid, Comment, Watchlist

# Eliminar datos existentes
User.objects.all().delete()
Category.objects.all().delete()
AuctionListing.objects.all().delete()
Bid.objects.all().delete()
Comment.objects.all().delete()
Watchlist.objects.all().delete()

# Crear usuarios de ejemplo
user1 = User.objects.create_user(username="user1", email="user1@example.com", password="password")
user2 = User.objects.create_user(username="user2", email="user2@example.com", password="password")
user3 = User.objects.create_user(username="user3", email="user3@example.com", password="password")

# Crear categorías de ejemplo
category1 = Category.objects.create(name="Electronics")
category2 = Category.objects.create(name="Fashion")
category3 = Category.objects.create(name="Home & Garden")

# URLs de las imágenes reales
image_url1 = 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTX7JT1uU-e9J_lXMjeFAZ8gDlI-C1jMAJ54aajSpcxI_gFuo4xXNMVk-xs2b9htSz3m84XvUSeRoGE0g4pVoTdCnMzS1sQzbpg-OWHszwJgCCSOM4xUDIOLQ'
image_url2 = 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQDw--Bi8CNkrNAxmS5e7GeyiKJ2ByNOx139Y7UWntNgKC-pcaMFmiKCvF0PGbbm-9cpltg0BWASCMDXNsdc79FW_8bV5XwOdYxru0l-h9Q6ciHiW2I35OPJtU'
image_url3 = 'https://www.gardeningexpress.co.uk/media/catalog/product/cache/fa4e57de89a0fb1427d2c82c53fb200f/3/_/3_7_1.jpg'

# Crear subastas de ejemplo con URLs de imágenes
listing1 = AuctionListing.objects.create(
    title="iPhone 12",
    description="A brand new iPhone 12.",
    starting_bid=700,
    category=category1,
    owner=user1,
    is_active=True,
    image_url=image_url1  # Asignar la URL de la imagen
)

listing2 = AuctionListing.objects.create(
    title="Designer Handbag",
    description="A stylish designer handbag.",
    starting_bid=300,
    category=category2,
    owner=user2,
    is_active=True,
    image_url=image_url2  # Asignar la URL de la imagen
)

listing3 = AuctionListing.objects.create(
    title="Garden Tools Set",
    description="A complete set of tools for your garden.",
    starting_bid=50,
    category=category3,
    owner=user3,
    is_active=True,
    image_url=image_url3  # Asignar la URL de la imagen
)

# Crear ofertas de ejemplo
Bid.objects.create(listing=listing1, bidder=user2, bid_amount=750)
Bid.objects.create(listing=listing2, bidder=user3, bid_amount=350)
Bid.objects.create(listing=listing3, bidder=user1, bid_amount=60)

# Crear comentarios de ejemplo
Comment.objects.create(listing=listing1, commenter=user3, comment_text="Is this available in different colors?")
Comment.objects.create(listing=listing2, commenter=user1, comment_text="What is the material of this handbag?")
Comment.objects.create(listing=listing3, commenter=user2, comment_text="How long is the warranty on these tools?")

# Agregar subastas a las listas de seguimiento de los usuarios
watchlist1 = Watchlist.objects.create(user=user1)
watchlist1.listings.add(listing2)

watchlist2 = Watchlist.objects.create(user=user2)
watchlist2.listings.add(listing3)

watchlist3 = Watchlist.objects.create(user=user3)
watchlist3.listings.add(listing1)

print("Sample data successfully populated!")
