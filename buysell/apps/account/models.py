from django.db import models
from django.conf import settings

from buysell.apps.post.models import Tag, Post

class UserProfile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribe_tag = models.ManyToManyField(Tag)
    profile_image = models.ImageField(upload_to = 'profile', default='default_profile.png')

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

class Message(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(null = False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                related_name = 'message_sender')
    receive_date = models.DateTimeField(auto_now_add = True)

class Transaction(models.Model):

    STATUS_TYPE = (
        ('request', 'REQUEST'),
        ('accept', 'ACCEPT'),
        ('deny', 'DENY'),
    )

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                related_name = 'transaction_seller')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    status = models.CharField(max_length = 10, choices = STATUS_TYPE)
    certified_date = models.DateTimeField()
