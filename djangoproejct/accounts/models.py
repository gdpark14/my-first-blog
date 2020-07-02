from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followers=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followings')

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    nickname=models.CharField(max_length=40,blank=True)
    introduction=models.TextField(blank=True)
    image = ProcessedImageField(
    	blank = True,
        upload_to = 'profile/images',
        processors = [ResizeToFill(300, 300)],
        format = 'JPEG',
        options = {'quality':90},
        ) 
