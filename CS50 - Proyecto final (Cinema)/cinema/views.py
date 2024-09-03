from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    today = timezone.now().date()
    one_year_ago = today - relativedelta(years=1)
    print("Today's date:", today)  # Esto imprimirá el valor de 'today' en la consola
    screenings = Screening.objects.filter(date_time__date=one_year_ago).order_by('date_time')
    return render(request, "cinema/index.html", {
        "movies": movies,
        "screenings" : screenings
    })

def movie_detail(request, id):
    movie = Movie.objects.get(pk=id)
    return render(request, 'cinema/movie.html', {'movie': movie})

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
            return render(request, "cinema/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cinema/login.html")
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cinema/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cinema/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cinema/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def screenings(request):
    today = timezone.now().date()

    # Obtener el parámetro de fecha si está presente
    selected_date = request.GET.get('date', None)
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = today

    screenings = Screening.objects.filter(date_time__date=selected_date).order_by('date_time')

    return render(request, 'cinema/screenings.html', {
        'screenings': screenings,
        'selected_date': selected_date,
    })

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    today = timezone.now().date()
    one_year_ago = today - relativedelta(years=1)
    print("Today's date:", today)  # Esto imprimirá el valor de 'today' en la consola
    screenings = Screening.objects.filter(date_time__date=one_year_ago).order_by('date_time')
    return render(request, "cinema/index.html", {
        "movies": movies,
        "screenings" : screenings
    })

def movie_detail(request, id):
    movie = Movie.objects.get(pk=id)
    return render(request, 'cinema/movie.html', {'movie': movie})

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
            return render(request, "cinema/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cinema/login.html")
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cinema/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cinema/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cinema/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def screenings(request):
    today = timezone.now().date()

    # Obtener el parámetro de fecha si está presente
    selected_date = request.GET.get('date', None)
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = today

    screenings = Screening.objects.filter(date_time__date=selected_date).order_by('date_time')

    return render(request, 'cinema/screenings.html', {
        'screenings': screenings,
        'selected_date': selected_date,
    })


def book_ticket(request, screening_id):
    screening = Screening.objects.get(pk=screening_id)
    if request.method == 'POST':
        seat_numbers = request.POST.getlist('seat_number')  # Obtener múltiples asientos
        for seat_number in seat_numbers:
            if Ticket.objects.filter(screening=screening, seat_number=seat_number).exists():
                messages.error(request, f'El asiento {seat_number} ya está reservado. Por favor, selecciona otro.')
                return redirect('book_ticket', screening_id=screening_id)

        for seat_number in seat_numbers:
            Ticket.objects.create(
                user=request.user,
                screening=screening,
                seat_number=seat_number
            )
        messages.success(request, 'Reserva realizada con éxito!')
        return redirect('user_tickets')

    taken_seats = Ticket.objects.filter(screening=screening).values_list('seat_number', flat=True)
    special_seats = ['A1', 'A7']  # Asientos especiales predefinidos
    print("Hello")
    print(request.user.is_authenticated == False) 
    context = {
        'screening': screening,
        'taken_seats': list(taken_seats),
        'special_seats': special_seats,
        'row_range': range(1, 6), 
        'seat_range': range(1, 11),  
        'is_authenticated': request.user.is_authenticated, 
    }
    return render(request, 'cinema/book_ticket.html', context)

@login_required
def complete_purchase(request, screening_id):
    screening = Screening.objects.get(pk=screening_id)
    if request.method == 'POST':
        seat_numbers = request.POST.get('seat_number', '').split(',')
        card_number = request.POST.get('card_number')
        card_expiration = request.POST.get('card_expiration')
        card_cvc = request.POST.get('card_cvc')
        print(f"Seat numbers received: {seat_numbers}")
        if not seat_numbers or seat_numbers == ['']:
            messages.error(request, "No se han seleccionado asientos.")
            return redirect('book_ticket', screening_id=screening_id)

        for seat_number in seat_numbers:
            if Ticket.objects.filter(screening=screening, seat_number=seat_number).exists():
                messages.error(request, f'El asiento {seat_number} ya está reservado. Por favor, selecciona otro.')
                return redirect('book_ticket', screening_id=screening_id)

        # Lógica para procesar el pago (omitir detalles específicos aquí)

        # Crear los tickets
        for seat_number in seat_numbers:
            Ticket.objects.create(
                user=request.user,
                screening=screening,
                seat_number=seat_number
            )

        messages.success(request, 'Compra realizada con éxito!')
        return redirect('user_tickets')

    # Si no es POST, redirigir de nuevo a la selección de asientos
    return redirect('book_ticket', screening_id=screening_id)


@login_required
def user_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).select_related('screening', 'screening__movie')
    return render(request, 'cinema/user_tickets.html', {'tickets': tickets})


@login_required
@require_POST
def refund_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    ticket.delete()
    return JsonResponse({'status': 'success'})

def movies_view(request):
    genres = Genre.objects.prefetch_related('movies').all()
    return render(request, 'cinema/movies.html', {
        'genres': genres,
    })

def upcoming_movies_view(request):
    upcoming_movies = Movie.objects.filter(is_released=False).order_by('release_date')
    return render(request, 'cinema/upcoming.html', {
        'upcoming_movies': upcoming_movies,
    })