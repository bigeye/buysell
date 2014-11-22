from django.contrib import admin
from buysell.apps.post.models import Tag, Post, Message, Review

class TagAdmin(admin.ModelAdmin):

    model = Tag

class PostAdmin(admin.ModelAdmin):
    model = Post

class MessageAdmin(admin.ModelAdmin):
    model = Message

class ReviewAdmin(admin.ModelAdmin):
    model = Review

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Review, ReviewAdmin)
