from django.contrib import admin

# Register your models here.
from .models import FollowerCount, LikePost, Profile ,Post , Comment

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowerCount)
admin.site.register(Comment)