from django.contrib import admin
from .models import User, Genre, Movie, Screening, Ticket
# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Screening)
admin.site.register(Ticket)