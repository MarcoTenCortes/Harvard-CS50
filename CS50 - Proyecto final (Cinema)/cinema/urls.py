
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('book/<int:screening_id>/', views.book_ticket, name='book_ticket'),
    path('screenings/', views.screenings, name='screenings'),
    path('book/<int:screening_id>/purchase/', views.complete_purchase, name='complete_purchase'),
    path('my-tickets/', views.user_tickets, name='user_tickets'),
    path('refund_ticket/<int:ticket_id>/', views.refund_ticket, name='refund_ticket'),
    path('movies/', views.movies_view, name='movies'),
    path('upcoming/', views.upcoming_movies_view, name='upcoming_movies'),
    #path('confirmation/<int:ticket_id>/', views.confirmation, name='confirmation'),
]
