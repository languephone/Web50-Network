from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def toggle_follow(self, following):
        """Adds or removes name to/from following list of user"""
        
        # First check if followlist already exists for follower
        if Follow.objects.filter(follower=self).exists():
            followlist = Follow.objects.get(follower=self.id)
            # Add user if not already in list
            if following not in followlist.following.all():
                followlist.following.add(following)
            # Remove user if already in list
            else:
                followlist.following.remove(following)
        # If followlist for user doesn't exist, create one then add post to list
        else:
            followlist = Follow(follower=self)
            followlist.save()
            followlist.following.add(following)

    def is_followed(self, following):
        """Returns True/False if user is already followed"""

        return Follow.objects.filter(follower=self).filter(following=following).exists()



class Post(models.Model):
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username}: '{self.content[:25]}...'"

    def count_likes(self):
        likes = len(Like.objects.filter(post=self.id))
        return likes

    def toggle_like(self, user):
        # First check if likelist already exists for user, then add/remove post
        if Like.objects.filter(user=user).exists():
            likelist = Like.objects.get(user=user)
            if self not in likelist.post.all():
                likelist.post.add(self)
            else:
                likelist.post.remove(self)
        # If likelist for user doesn't exist, create one then add post to list
        else:
            likelist = Like(user=user)
            likelist.save()
            likelist.post.add(self)

    def is_liked(self, user):
        """Return true if post already liked by user."""

        return Like.objects.filter(user=user).filter(post=self).exists()

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user.username,
            "date": self.date,
            "likes": self.count_likes()
        }


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} likelist"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="follower_username")
    following = models.ManyToManyField(User, blank=True,
        related_name="following_username")
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower.username}'s following list."
