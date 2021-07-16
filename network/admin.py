from django.contrib import admin

from .models import User, Post, Like

# Register your models here.
class LikeAdmin(admin.ModelAdmin):
	list_display = ("user", "post", "date")

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like, LikeAdmin)