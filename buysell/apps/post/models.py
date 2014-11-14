from django.db import models
from django.conf import settings

class Tag(models.Model):
    
    name = models.TextField()

class Post(models.Model):

    POST_TYPE = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )

    post_type = models.CharField(max_length = 10, choices = POST_TYPE)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length = 150)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add = True)
    update_date = models.DateTimeField(auto_now = True, auto_now_add = True)
    tags = models.ManyToManyField(Tag)

class Comment(models.Model):

    post = models.ForeignKey(Post)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add = True)

