from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


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

