from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    genres = models.ManyToManyField(Genre, related_name="movies")
    image_url = models.URLField(blank=True, null=True) 
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    is_released = models.BooleanField(default=False, help_text="Indicates if the movie is released and tickets can be purchased")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        release_date = self.release_date
        if isinstance(release_date, datetime):
            release_date = release_date.date()

        if release_date <= timezone.now().date():
            self.is_released = True
        else:
            self.is_released = False
        super(Movie, self).save(*args, **kwargs)

class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="screenings")
    date_time = models.DateTimeField()
    auditorium = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.movie.title} at {self.date_time}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name="tickets")
    seat_number = models.CharField(max_length=10)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.screening.movie.title} on {self.screening.date_time} (Seat: {self.seat_number})"
