import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like


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

    # Code below runs when method is GET
    posts = Post.objects.all().order_by('-date')

    # Convert posts query set into JSON using serialize method
    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required(login_url='/login')
def like(request):
    if request.method == "GET":
        related_post = Post.objects.get(pk=int(request.GET["post"]))


    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post")
        related_post = Post.objects.get(pk=int(post_id))
        related_post.toggle_like(request.user)
        return JsonResponse({"message": "Like saved successfully."}, status=201)