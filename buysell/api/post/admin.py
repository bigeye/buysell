from django.contrib import admin
from buysell.api.post.models import Tag, Post, Message, Review, PostImage, \
        Transaction

class TagAdmin(admin.ModelAdmin):
    model = Tag

class PostImageAdmin(admin.ModelAdmin):
    model = PostImage

class PostAdmin(admin.ModelAdmin):
    model = Post

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction

class MessageAdmin(admin.ModelAdmin):
    model = Message

class ReviewAdmin(admin.ModelAdmin):
    model = Review

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Transaction, TransactionAdmin)
