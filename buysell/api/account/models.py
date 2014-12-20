from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from buysell.api.post.models import Tag, Post

class UserProfile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', unique=True)
    subscribe_tag = models.ManyToManyField(Tag)
    profile_image = models.ImageField(upload_to = 'profile', default='default_profile.png')
    phone = models.CharField(max_length = 50)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class OAuthToken(models.Model):

    SNS_TYPE = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    sns_type = models.CharField(max_length = 10, choices = SNS_TYPE)
    token = models.TextField()

class Notification(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(null = False)
    receive_date = models.DateTimeField(auto_now_add = True)
