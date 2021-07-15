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

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user.username,
            "date": self.date
        }


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} likes '{self.post.content[:25]}...'"