from buysell.api.post.models import Post, Transaction, Message, Review, Tag, PostImage
from buysell.api.account.serializers import UserSerializer
from buysell import settings

from rest_framework import serializers

class PostImageSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = PostImage
        fields = ('url', 'alert')

    def get_url(self, obj):
        return obj.image.url

class TagSerialzier(serializers.ModelSerializer):
    pass

class PostSerializer(serializers.ModelSerializer):

    images = PostImageSerializer(many=True, required=False)
    writer = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'writer', 'title', 'content', 'is_private', 
                'create_date', 'update_date', 'images')

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.title = attrs.get('title', instance.title)
            if (attrs.get('is_private', None) is not None):
                instance.is_private = True if attrs['is_private'] else False
            instance.content = attrs.get('content', instance.content)
            return instance

        request = self.context.get('request', None)

        is_private = False
        if attrs.get('is_private', None) is not None:
            is_private = True if attrs['is_private'] else False

        instance = Post(writer = self.context['request'].user,
                title = attrs['title'],
                is_private = is_private,
                content = attrs['content'])

        return instance

class TransactionSerializer(serializers.ModelSerializer):

    status = serializers.CharField()
    requester = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    
    def validate(self, attrs):
        obj = Transaction.objects.filter(post=self.context['post'],
                requester=self.context['request'].user) 

        if obj.exists():
            raise serializers.ValidationError('User already requested a transaction')
        else:
            return attrs

    def restore_object(self, attrs, instance=None):
        assert instance is None, 'Transaction cannot be updated after creation'
        return Transaction(post=self.context['post'],
                requester=self.context['request'].user,
                status=attrs['status'])

    class Meta:
        model = Transaction

class MessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)
    transaction = TransactionSerializer()

    class Meta:
        model = Message

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
