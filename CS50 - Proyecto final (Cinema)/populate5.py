import os
import django
from datetime import datetime, timedelta
import random

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalProjec.settings')
django.setup()

from cinema.models import Genre, Movie, Screening

# Crear o obtener géneros
action = Genre.objects.get_or_create(name="Action")[0]
animation = Genre.objects.get_or_create(name="Animation")[0]
drama = Genre.objects.get_or_create(name="Drama")[0]
fantasy = Genre.objects.get_or_create(name="Fantasy")[0]
crime = Genre.objects.get_or_create(name="Crime")[0]
thriller = Genre.objects.get_or_create(name="Thriller")[0]

# Lista de películas disponibles
available_movies = [
    {
        "title": "Digimon: The Movie",
        "description": """A young boy and his friends discover the digital world, where they encounter strange creatures 
        known as Digimon. Together, they must protect both the digital and real worlds from an evil force.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 85,
        "genres": [animation, action],
        "image_url": "https://es.web.img3.acsta.net/medias/nmedia/18/93/58/70/20265714.jpg",
        "price": 7.99,
        "is_released": True
    },
    {
        "title": "Avengers: Endgame",
        "description": """After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help 
        of remaining allies, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 181,
        "genres": [action, drama],
        "image_url": "https://hips.hearstapps.com/hmg-prod/images/poster-vengadores-endgame-1552567490.jpg",
        "price": 12.99,
        "is_released": True
    },
    {
        "title": "BoJack Horseman",
        "description": """BoJack Horseman, a humanoid horse and washed-up TV star, struggles with depression, addiction, and 
        maintaining relationships. The series explores his life as he attempts to find meaning and redemption in his career and personal life.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 25,
        "genres": [drama, animation],
        "image_url": "https://es.web.img2.acsta.net/pictures/15/02/20/10/21/222923.jpg",
        "price": 5.99,
        "is_released": True
    },
    {
        "title": "Cyberpunk: Edgerunners",
        "description": """In a dystopian future where mega-corporations dominate the world, a street kid tries to survive 
        by becoming an edgerunner—a mercenary outlaw with enhanced cybernetic abilities.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 120,
        "genres": [action, animation],
        "image_url": "https://es.web.img2.acsta.net/pictures/20/06/29/10/22/2148622.jpg",
        "price": 8.99,
        "is_released": True
    },
    {
        "title": "Joker",
        "description": """Joker tells the story of Arthur Fleck, a failed stand-up comedian in Gotham City who descends into 
        madness and transforms into the criminal mastermind known as the Joker.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 122,
        "genres": [crime, drama],
        "image_url": "https://destinoarrakis.com/wp-content/uploads/2019/10/fhjfepfh43q21.jpg",
        "price": 9.99,
        "is_released": True
    },
    {
        "title": "The Dark Knight",
        "description": """With the help of allies such as Commissioner Gordon and Harvey Dent, Batman has been able to keep 
        a tight lid on crime in Gotham City. But when a vile young criminal calling himself the Joker suddenly throws the town into chaos, the caped Crusader begins to tread a fine line between heroism and vigilantism.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 152,
        "genres": [action, crime, thriller],
        "image_url": "https://www.mubis.es/media/covers/2115/4386/el-caballero-oscuro-portada-l_cover.jpg",
        "price": 10.99,
        "is_released": True
    },
    {
        "title": "Harry Potter and the Order of the Phoenix",
        "description": """With his fifth year of study at Hogwarts, Harry Potter discovers that much of the wizarding community 
        has been denied the truth about his recent encounter with the evil Lord Voldemort. The Ministry of Magic refuses to believe in Voldemort's return and wages a smear campaign against Harry and Dumbledore.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 138,
        "genres": [fantasy, drama],
        "image_url": "https://static.wikia.nocookie.net/esharrypotter/images/2/23/Tt0373889_largeCover.jpg/revision/latest?cb=20110815230703",
        "price": 11.99,
        "is_released": True
    },
    {
        "title": "The Hobbit: The Battle of the Five Armies",
        "description": """Bilbo Baggins is in a desperate attempt to prevent Smaug from raining his fiery wrath down upon the 
        defenseless men, women, and children of Lake-town. Meanwhile, Thorin Oakenshield sacrifices friendship and honor in his search for the Arkenstone.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 144,
        "genres": [fantasy, action],
        "image_url": "https://es.web.img2.acsta.net/pictures/14/10/17/13/10/188874.jpg",
        "price": 10.99,
        "is_released": True
    },
    {
        "title": "Fight Club",
        "description": """An insomniac office worker looking for a way to change his life crosses paths with a devil-may-care 
        soap maker, forming an underground fight club that evolves into something much, much more.""",
        "release_date": datetime.now() - timedelta(days=365),
        "duration": 139,
        "genres": [drama, thriller],
        "image_url": "https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_.jpg",
        "price": 9.99,
        "is_released": True
    }
]

# Lista de películas próximas
upcoming_movies = [
    {
        "title": "Harry Potter and the Half-Blood Prince",
        "description": """As Harry Potter begins his sixth year at Hogwarts, he discovers an old book marked as 
        "the property of the Half-Blood Prince" and begins to learn more about Lord Voldemort's dark past.""",
        "release_date": datetime.now() + timedelta(days=30),
        "duration": 153,
        "genres": [fantasy, drama],
        "image_url": "https://www.aceprensa.com/wp-content/uploads/2009/07/767-0.jpg",
        "price": 11.99,
        "is_released": False
    },
    {
        "title": "Your Name",
        "description": """Two teenagers share a profound, magical connection upon discovering they are swapping bodies. 
        Things manage to become even more complicated when the boy and girl decide to meet in person.""",
        "release_date": datetime.now() + timedelta(days=45),
        "duration": 106,
        "genres": [animation, fantasy, drama],
        "image_url": "https://imgsrv.crunchyroll.com/cdn-cgi/image/fit=contain,format=auto,quality=85,width=480,height=720/catalog/crunchyroll/c9947dfac4b57728c3c7eb81ed77ac09.jpe",
        "price": 8.99,
        "is_released": False
    }
]

# Crear películas disponibles y screenings en diferentes días y horarios
for movie_data in available_movies:
    movie = Movie.objects.create(
        title=movie_data["title"],
        description=movie_data["description"],
        release_date=movie_data["release_date"],
        duration=movie_data["duration"],
        image_url=movie_data["image_url"],
        price=movie_data["price"],
        is_released=movie_data["is_released"]
    )
    movie.genres.set(movie_data["genres"])
    movie.save()

    # Crear screenings para las películas lanzadas en diferentes días y horarios
    for i in range(5):
        screening_date = datetime.now() + timedelta(days=i)
        screening_time = screening_date.replace(hour=random.randint(10, 22), minute=random.choice([0, 15, 30, 45]))
        Screening.objects.create(
            movie=movie,
            date_time=screening_time,
            auditorium=f"Auditorium {random.randint(1, 5)}"
        )

# Crear películas próximas
for movie_data in upcoming_movies:
    movie = Movie.objects.create(
        title=movie_data["title"],
        description=movie_data["description"],
        release_date=movie_data["release_date"],
        duration=movie_data["duration"],
        image_url=movie_data["image_url"],
        price=movie_data["price"],
        is_released=movie_data["is_released"]
    )
    movie.genres.set(movie_data["genres"])
    movie.save()

print("Database populated with movies and screenings!")
