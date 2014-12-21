from django.core.exceptions import ValidationError

from buysell.api.post.models import Post, Transaction, Message, Review, Tag, PostImage
from buysell.api.account.serializers import UserSerializer
from buysell import settings

from rest_framework import serializers

class PostImageSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField('get_url')
    post = serializers.SerializerMethodField('get_post')

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.alert = attrs['alert']
            instnace.iamge = attrs['image']
        else:
            instance = PostImage(post=self.context['post'],
                    alert=attrs['alert'],
                    image=attrs['image'])
        return instance

    class Meta:
        model = PostImage
        fields = ('url', 'alert', 'image', 'post')

    def get_url(self, obj):
        return obj.image.url

    def get_post(self, obj):
        return obj.post.id

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag

class PostSerializer(serializers.ModelSerializer):

    images = PostImageSerializer(many=True, required=False)
    writer = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'status_type', 'writer', 'title', 'content', 'price', 'is_private', 
                'create_date', 'update_date', 'images', 'tags')

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.title = attrs.get('title', instance.title)
            if (attrs.get('is_private', None) is not None):
                instance.is_private = True if attrs['is_private'] else False
            instance.content = attrs.get('content', instance.content)
            instance.price = attrs.get('price', instance.price)
            instance.status_type = attrs.get('status_type', instance.status_type)
            return instance

        request = self.context.get('request', None)

        is_private = False
        if attrs.get('is_private', None) is not None:
            is_private = True if attrs['is_private'] else False

        instance = Post(status_type = attrs['status_type'],
                writer = self.context['request'].user,
                title = attrs['title'],
                price = attrs['price'],
                is_private = is_private,
                content = attrs['content'])

        return instance

class TransactionSerializer(serializers.ModelSerializer):

    requester = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    
    def restore_object(self, attrs, instance=None):
        if instance is not None:
            # Update only transaction status
            next_status = attrs.get('status', None)
            instance.status = next_status
        else:
            # Create user transaction
            instance = Transaction(post=self.context['post'],
                    requester=self.context['request'].user,
                    status=attrs['status'])

        return instance

    class Meta:
        model = Transaction

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review

    def validate(self, attrs):
        pass

    def restore_object(self, attrs, instance=None):
        assert instance is None, 'Review cannot be updated after creation'
        pass


class MessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)
    post = serializers.SerializerMethodField('get_post')
    transaction = TransactionSerializer(read_only=True)

    def get_post(self, obj):
        return PostSerializer(obj.transaction.post).data

    def restore_object(self, attrs, instance=None):
        assert instance is None
        return Message(transaction=self.context['transaction'],
                message_type=attrs.get('message_type', 'normal'),
                sender=self.context['request'].user,
                content=attrs['content'])

    class Meta:
        model = Message
        fields = ('sender', 'content', 'receive_date', 'post', 'message_type', 'transaction')

