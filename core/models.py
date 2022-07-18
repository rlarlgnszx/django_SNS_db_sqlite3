
from pyexpat import model
from django.db import models

from django.contrib.auth import get_user_model
import uuid 
from datetime import datetime
User = get_user_model()
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg= models.ImageField(upload_to='profile_images',default ="profile.jpg")
    location = models.CharField(max_length=100,blank=True)

    def __str__(self): 
        return self.user.username
class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    #! uuid => 유니크 아이디 생성 primarykey =True
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default = datetime.now)
    no_of_likes = models.IntegerField(default =0)

    def user_img(self):
        user = User.objects.filter(username=self.user).first()
        return Profile.objects.filter(id_user=user.id)

    user_profileimg = property(user_img)

    def comment_check(self):
        return Comment.objects.filter(post_id=self.id)

    comments = property(comment_check)

    def __len__(self):
        return len(self.comments)
    

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username= models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)


    def __str__(self):
        return self.user

class Comment(models.Model):
    comment = models.CharField(max_length=150)
    user_id = models.CharField(max_length=100)
    post_id = models.CharField(max_length=100)

    def get_profile(self):
        get_profile_imge = Profile.objects.filter(id_user=self.user_id)
        return get_profile_imge

    user_profileimg= property(get_profile)

    def __str__(self):
        return self.post_id