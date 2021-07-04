from datetime import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.template.defaulttags import register
from .models import User, Post, Like, Follow
from django.views.decorators.csrf import csrf_exempt

#below function is for template filtering, check out "like button" section on index, profile or following HTML files.
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request, page=1):
    start = 0
    end = 0
    previous = 0

    if page == 1:
        start = 0
        end = 10
    else:
        end = page * 10
        start = end - 10
        previous = page - 1


    posts = Post.objects.all().order_by('created').reverse()[start:end]
    user = request.user

    postLikesTotal = {}
    userLikes = {}

    for p in posts:
        likes = Like.objects.filter(post_id = p.id)
        if likes:
            postLikesTotal[p.id] = len(likes)
        else:
            postLikesTotal[p.id] = 0

        userLike = Like.objects.filter(user_id = user.id).filter(post_id = p.id)
        if userLike:
            userLikes[p.id] = True
        else:
            userLikes[p.id] = False

    return render(request, "network/index.html", {
        "posts": posts,
        "postLikesTotal": postLikesTotal,
        "userLikes": userLikes,
        "next": page + 1,
        "previous": previous,
    })

@csrf_exempt
@login_required
def likeUnlike(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        return JsonResponse({"error":"No post found with this id"}, status=404)

    user = request.user

    is_liked = Like.objects.filter(post_id=post_id).filter(user_id=user.id)
    if is_liked:
        is_liked.delete()
        return JsonResponse({"is_liked": False}, status=200)
    else:
        userLike = Like()
        userLike.user = user
        userLike.post = post
        userLike.save()
        return JsonResponse({"is_liked": True}, status=200)

    
@csrf_exempt
@login_required
def newPost(request):
    user = request.user

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    postContent = body = data.get("content", "")

    if postContent == "" or not postContent:
        return JsonResponse({"error": "Post content can not be empty."}, status=400)

    newpost = Post()
    newpost.user = user
    newpost.content = postContent
    newpost.created = datetime.now()
    newpost.updated = datetime.now()
    newpost.save()

    return JsonResponse({"post_id": newpost.id, "userName": user.username, "created": newpost.created, "content": postContent}, status=200)


def profile(request, user_id, page=1):
    try:
        profileUser = User.objects.get(id=user_id)
    except:
        return HttpResponse("No such user")

    start = 0
    end = 0
    previous = 0

    if page == 1:
        start = 0
        end = 10
    else:
        end = page * 10
        start = end - 10
        previous = page - 1

    userPosts = Post.objects.filter(user_id = profileUser.id).order_by('created').reverse()[start:end]

    userFollowers = Follow.objects.filter(followedUser = profileUser.id).count()

    following = Follow.objects.filter(user_id = profileUser.id).count()

    is_following = Follow.objects.filter(user_id = request.user.id, followedUser=profileUser.id)

    if len(is_following) > 0:
        is_following = True
    else:
        is_following = False

    postLikesTotal = {}
    userLikes = {}

    for p in userPosts:
        likes = Like.objects.filter(post_id = p.id)
        if likes:
            postLikesTotal[p.id] = len(likes)
        else:
            postLikesTotal[p.id] = 0

        userLike = Like.objects.filter(user_id = request.user.id).filter(post_id = p.id)
        if userLike:
            userLikes[p.id] = True
        else:
            userLikes[p.id] = False

    return render(request, "network/profile.html", {
        "profileUser": profileUser,
        "userPosts": userPosts,
        "userFollowers": userFollowers,
        "following": following,
        "is_following": is_following,
        "postLikesTotal": postLikesTotal,
        "userLikes": userLikes,
        "next": page + 1,
        "previous": previous,
    })


@csrf_exempt
@login_required
def follow(request, profile_user_id):
    user = request.user
    try:
        profile_user = User.objects.get(id=profile_user_id)
    except:
        return HttpResponse("No such user")

    if user.id == profile_user.id:
        return JsonResponse({"error":"You can't follow yourself."}, status=400)

    is_following = Follow.objects.filter(user_id = user.id, followedUser = profile_user.id)

    follow = False

    if len(is_following) > 0:
        is_following.delete()
    else:
        newFollow = Follow()
        newFollow.user = user
        newFollow.followedUser = profile_user
        newFollow.save()

        follow = True
    
    return JsonResponse({"is_following":follow}, status=200)


@login_required
def following(request, page=1):
    user = request.user

    start = 0
    end = 0
    previous = 0

    if page == 1:
        start = 0
        end = 10
    else:
        end = page * 10
        start = end - 10
        previous = page - 1

    #this query gets a list of user_ids of user's follows
    userFollowingUser_ids = Follow.objects.filter(user_id = user.id).values_list('followedUser', flat=True)

    #this query filters all post which user_ids are in "userFollowingUser_ids" list we get above
    #and also we slice it acoording to page number user requested
    followingsPosts = Post.objects.filter(user_id__in = userFollowingUser_ids).order_by('created').reverse()[start:end]
       
    postLikesTotal = {}
    userLikes = {}

    for p in followingsPosts:
        likes = Like.objects.filter(post_id = p.id)
        if likes:
            postLikesTotal[p.id] = len(likes)
        else:
            postLikesTotal[p.id] = 0

        userLike = Like.objects.filter(user_id = user.id).filter(post_id = p.id)
        if userLike:
            userLikes[p.id] = True
        else:
            userLikes[p.id] = False

    return render(request, "network/following.html", {
        "posts": followingsPosts,
        "postLikesTotal": postLikesTotal,
        "userLikes": userLikes,
        "next": page + 1,
        "previous": previous,
    })


@csrf_exempt
@login_required
def editPost(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        return HttpResponse("No such a post")

    user = request.user

    if user.id != post.user_id:
        return JsonResponse({"result":False, "message":"You can't edit another user's post."}, status=403)
    
    data = json.loads(request.body)

    postContent = body = data.get("content", "")

    try:
        post.content = postContent
        post.updated = datetime.now()
        post.save()
    except:
        return JsonResponse({"result":False, "message":"Something went wrong, please refresh the page and try again."}, status=500)

    return JsonResponse({"result":True, "message":"Post updated successfully"}, status=200)


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
