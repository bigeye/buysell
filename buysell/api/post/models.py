from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Tag(models.Model):
    
    name = models.TextField(unique=True)

class Post(models.Model):

    STATUS_TYPE = (
        ('available' , 'Available'),
        ('reserved' , 'Reserved'),
        ('finish' , 'Finished'),
    )

    status_type = models.CharField(max_length = 10, choices = STATUS_TYPE)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 150)
    create_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True, auto_now_add = True)
    is_private = models.BooleanField(default = False)
    tags = models.ManyToManyField(Tag, blank=True)

    #template = models.TextField()
    content = models.TextField()

class PostImage(models.Model):
    image = models.ImageField(upload_to = 'post')
    alert = models.CharField(max_length = 150)
    post = models.ForeignKey(Post, related_name = 'images')

class Transaction(models.Model):

    STATUS_TYPE = (
        ('ask', 'ASK'),
        ('request', 'REQUEST'),
        ('pending', 'PENDING'),
        ('accept', 'ACCEPT'),
        ('deny', 'DENY'),
        ('cancel', 'CANCEL'),
    )

    requester = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    status = models.CharField(max_length = 10, choices = STATUS_TYPE, default='ask')
    request_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = (('requester', 'post'))

class Message(models.Model):

    MSG_TYPE = (
        ('st_update','ST_UPDATE'),
        ('normal', 'NORMAL'),
    )

    message_type = models.CharField(max_length = 10, choices = MSG_TYPE, default='normal')
    transaction = models.ForeignKey(Transaction)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(null = False)
    receive_date = models.DateTimeField(auto_now_add = True)

    def clean(self):
        """Semantic check for Message model
        """
        if self.sender not in (self.transaction.requester, 
                self.transaction.post.writer):
            raise ValidationError('Message should be sent from either ' + \
                    'post writer or transaction requester')


class Review(models.Model):

    transaction = models.OneToOneField(Transaction)
    content = models.TextField()
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'reviewer')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'reviewee')
    written_date = models.DateTimeField(auto_now_add = True)
