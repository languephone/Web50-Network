import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow

def pagination(posts, request):
    """Return page numbers and limit posts per page"""
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def index(request):

    # Return all posts
    posts = Post.objects.all().order_by('-date')
    page_obj = pagination(posts, request)
    
    # Get list of user's liked posts (for logged-in users)
    like_list = []
    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user).exists():
            like_list = Like.objects.get(user=request.user).post.all()

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "like_list": like_list
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


@csrf_exempt
def posts(request):
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        new_post = Post(user=request.user, content=data["content"])
        new_post.save()
        return JsonResponse(new_post.content, safe=False)

    elif request.method =="PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=int(data["id"]))
        
        # ensure editor is the original poster
        if request.user != post.user:
            print("wrong user!")
            return JsonResponse(json.dumps(f"You cannot edit {post.user}'s post."), safe=False)
        
        post.content = data['content']
        post.save()
        return JsonResponse(post.content, safe=False)


@csrf_exempt
@login_required(login_url='/login')
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        related_post = Post.objects.get(pk=int(data["id"]))
        related_post.toggle_like(request.user)
        current_likes = related_post.count_likes()
        is_liked = related_post.is_liked(request.user)
        response = {'current_likes': current_likes, 'is_liked': is_liked}
        return JsonResponse(response, safe=False)


@csrf_exempt
@login_required(login_url='/login')
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        following = User.objects.get(username=data["username"])
        follower = request.user
        follower.toggle_follow(following)
        followers_count = following.count_followers()
        is_followed = follower.is_followed(following)
        response = {'followers_count': followers_count, 'is_followed': is_followed}
        return JsonResponse(response, safe=False)


@login_required(login_url='/login')
def following(request):
    # Return posts only from users the requester is following
    following = Follow.objects.get(follower=request.user.id).following.all()
    posts = Post.objects.filter(user__in=following).order_by('-date')
    page_obj = pagination(posts, request)

    # Get list of user's liked posts (for logged-in users)
    like_list = []
    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user).exists():
            like_list = Like.objects.get(user=request.user).post.all()

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "like_list": like_list
    })



def profile(request, username):

    # Return all posts from user
    posts = Post.objects.filter(user__username=username).order_by('-date')
    profile = User.objects.get(username=username)
    page_obj = pagination(posts, request)

    # Get list of user's liked posts (for logged-in users)
    like_list = []
    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user).exists():
            like_list = Like.objects.get(user=request.user).post.all()

    # Logic for follow/unfollow/none button in profile.html
    if request.user.is_authenticated:
        button = request.user.username != username
        followed = request.user.is_followed(profile)
    else:
        button = False
        followed = False

    following_count = profile.count_following()
    followers_count = profile.count_followers()

    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "button": button,
        "followed": followed,
        "username": username,
        "following_count": following_count,
        "followers_count": followers_count,
        "like_list": like_list
    })