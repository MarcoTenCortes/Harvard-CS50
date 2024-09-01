
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like

def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": posts,
        "posts_of_the_page":posts_of_the_page
    })

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
@csrf_exempt
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post(
            user=request.user,
            content=data.get("content", "")
        )
        post.save()
        return JsonResponse({"message": "Post created successfully."}, status=201)
    
@login_required
@csrf_exempt
def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})



@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = user.posts.all().order_by("-timestamp")
    following = Follow.objects.filter(follower=user).count()
    followers = Follow.objects.filter(following=user).count()
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    return render(request, "network/profile.html", {
        "profile_user": user,
        "posts": posts,
        "following": following,
        "followers": followers,
        "is_following": is_following
    })

@login_required
@csrf_exempt
def follow_toggle(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    follow = Follow.objects.filter(follower=request.user, following=target_user)

    if follow.exists():
        follow.delete()
        return JsonResponse({"message": "Unfollowed successfully."}, status=200)
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        return JsonResponse({"message": "Followed successfully."}, status=201)

@login_required
@csrf_exempt
def like_toggle(request, post_id):
    post = Post.objects.get(pk=post_id)
    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
        return JsonResponse({"message": "Like removed."}, status=200)
    else:
        Like.objects.create(user=request.user, post=post)
        return JsonResponse({"message": "Post liked."}, status=201)
    
@login_required
@csrf_exempt
def following(request):
    current_user = request.user
    following_people = Follow.objects.filter(follower=current_user).values_list('following', flat=True)
    
    following_posts = Post.objects.filter(user__in=following_people).order_by("-timestamp")
    
    
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts_of_the_page": posts_of_the_page
    })
