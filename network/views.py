from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):

    # Return all posts
    posts = Post.objects.all().order_by('-date')

    return render(request, "network/index.html", {
        "posts": posts
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


def posts(request):
    if request.method == "POST":
        new_post = Post(user=request.user, content=request.POST["post-text"])
        new_post.save()
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login')
def like(request):
    if request.method == "POST":
        related_post = Post.objects.get(pk=int(request.POST["post"]))
        new_like = Like(user=request.user, post=related_post)
        new_like.save()
        return HttpResponseRedirect(reverse("index"))


def profile(request, username):

    # Return all posts from user
    posts = Post.objects.filter(user__username=username).order_by('-date')
    
    following_list = Follow.objects.get(follower__username=username).following.all()
    following_count = len(following_list)
    followers_list = Follow.objects.filter(following__username=username)
    followers_count = len(followers_list)

    return render(request, "network/profile.html", {
        "posts": posts,
        "username": username,
        "following_count": following_count,
        "followers_count": followers_count
    })