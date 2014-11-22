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
    writer = UserSerializer(required=True)

    class Meta:
        model = Post
        fields = ('id', 'writer', 'title', 'content', 'create_date', 'update_date', 'images')

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.title = attrs.get('title', instance.title)
            if (attrs.get('is_private', None) is not None):
                instance.is_private = True if attrs['is_private'] else False
            instance.content = attrs.get('content', instance.content)
            return instance

        instance = Post(writer = self.request['context'].user,
                title = attrs['title'],
                is_private = True if attrs['is_private'] == 'true' else False,
                content = attrs['content'])

        return instance

class PostRetreiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'writer', 'title', 'content', 'create_date', 'update_date', 'images')
        # fields = ('writer', 'title', 'content', 'create_date', 'update_date', 'images')

    # def restore_object(self, attrs, instance=None):
    #     pass
    # post_id = serializers.IntegerField()

    # def validate(self, attrs):
    #     post = Post.objects.get(id=attrs['post_id'])
    #     return post
