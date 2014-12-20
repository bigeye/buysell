from django.http import Http404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from buysell.api.post.serializers import PostSerializer, TransactionSerializer,\
        MessageSerializer, PostImageSerializer
from buysell.api.post.models import Post, Transaction, PostImage

class IsPostOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.post.writer == request.user


class IsTransactionHolder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user in (obj.requester, obj.post.writer)


class PostCreateHandler(APIView):
    """**PostCreateHandler** class creates post

    ## Request ##
        :::bash
        $ curl -X POST "http://example.com/api/post/"
            -d '{"content" : "This is content", "title" : "This is title"}
            -H "Content-type: application/json"
    """

    def post(self, request, post_id=None, format=None):
        serializer = PostSerializer(data=request.DATA, context={
            'request' : request
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostImageCreateHandler(APIView):

    serializer_class = PostImageSerializer

    def post(self, request, post_id=None, format=None):
        """Post a new image to the post"""
        post = Post.objects.get(id=post_id)
        img_serializer = PostImageSerializer(data=request.DATA, files=request.FILES,
                context={'post' : post})

        if img_serializer.is_valid():
            img_serializer.save()
            return Response(img_serializer.data, status=status.HTTP_201_CREATED)
        return Response(img_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostImageHandler(APIView):

    permission_classes = (IsPostOwner,)

    def get_post_image(self, image_id):
        try:
            post_image = PostImage.objects.get(id=image_id)
            return post_image
        except PostImage.DoesNotExist:
            return None

    def check_post_has_image(self, post_id, post_image):
        return post_id == post_image.post.id
    
    def get(self, request, post_id=None, image_id=None, format=None):
        post_image = self.get_post_image(image_id)
        if post_image == None:
            return Response({'detail' : 'Image does not exist'},
                    status=status.HTTP_404_NOT_FOUND)

        if not self.check_post_has_image(int(post_id), post_image):
            return Response({'detail' : 'Post does not have the image'},
                    status=status.HTTP_400_BAD_REQUEST)

        img_serializer = PostImageSerializer(post_image)
        return Response(img_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id=None, image_id=None, format=None):
        post_image = self.get_post_image(image_id)
        if post_image == None:
            return Response({'detail' : 'Image does not exist'}, 
                    status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post_image)
        img_serializer = PostImageSerializer(post_image)
        post_image.delete()
        return Response(img_serializer.data, status=status.HTTP_200_OK)


class PostHandler(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_id=None, format=None):
        serializer = PostSerializer(self.get_object(post_id))
        return Response(serializer.data)

    def put(self, request, post_id=None, format=None):

        post = self.get_object(post_id)

        p_serializer = PostSerializer(post, data=request.DATA, partial=True)
        if p_serializer.is_valid():
            p_serializer.save()
            return Response(p_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(p_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class PostListHandler(ListAPIView):

    serializer_class = PostSerializer
    queryset = serializer_class.Meta.model.objects.all()
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by_param = '100'

    permission_classes = (permissions.AllowAny,)


class TransactionCreateHandler(APIView):

    def post(self, request, post_id=None, format=None):
        """Create Transaction if there is no transaction created by user.
        """
        try:
            post = Post.objects.get(id=post_id)

        except Post.DoesNotExist:
            return Response({
                'detail' : 'No post exists'
                }, status=status.HTTP_400_BAD_REQUEST)

        t_serializer = TransactionSerializer(data=request.DATA, context={
            'request' : request,
            'post' : post,
        })

        try:
            if t_serializer.is_valid():
                t_serializer.save()
                return Response(t_serializer.data, status=status.HTTP_200_OK)
            return Response(t_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({
                'detail' : 'User already request transaction for the post'
                }, status=status.HTTP_400_BAD_REQUEST)



class TransactionHandler(APIView):
    """**TransactionHandler** class handles transaction requests

    ## Requset
        :::bash
        $ curl -X GET "http://example.com/post/{post_id}/transaction.json"
                -H "Content-type: application/json"
    """

    permission_classes = (IsTransactionHolder,)

    def get_transaction(self, t_id):
        try:
            transaction = Transaction.objects.get(id=t_id)
            return transaction
        except Transaction.DoesNotExist:
            return None

    def get(self, request, transaction_id=None, format=None):
        """Get Transaction when there is transaction created by user."""
        transaction = self.get_transaction(transaction_id)
        if transaction is None:
            return Response({
                'detail' : 'Transaction dose not exist'
                }, status = status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, transaction)
        t_serializer = TransactionSerializer(transaction)
        return Response(t_erializer.data, status=status.HTTP_200_OK)

    def put(self, request, transaction_id=None, format=None):
        """Update Transaction"""
        transaction = self.get_transaction(transaction_id)
        if transaction is None:
            return Response({
                'detail' : 'Transaction dose not exist'
                }, status = status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, transaction)
        t_serializer = TransactionSerializer(transaction, data=request.DATA,
                partial=True)

        if t_serializer.is_valid():
            t_serializer.save()
            return Response(t_serializer.data, status=status.HTTP_200_OK)

        return Response(t_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class TransactionListHandler(ListAPIView):

    serializer_class = PostSerializer
    queryset = serializer_class.Meta.model.objects.all()
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by_param = '100'


class ReviewHandler(APIView):

    def get(self, request, post_id=None, format=None):
        """Get Review of Transaction if the review exists.
        """
        try:
            review = Review.objects.get(id=review_id)
            r_serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Http404

    def post(self, request, format=None):
        """Create Reivew of Transaction if the tranaction is finished and no
        review is written.
        """
        try:
            transaction = Transaction.objects.get(post__id=post_id)
        except Post.DoesNotExist:
            return Http404

        r_serializer = ReviewSerializer(data=request.DATA, context = {
            'request' : request,
            'transaction' : transaction,
        })

        if r_serializer.is_valid():
            r_serializer.save()
            return Response(r_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(r_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageCreateHandler(APIView):

    def post(self, request, transaction_id=None, format=None):
        """Create a new message on the transaction."""

        try:
            transaction = Transaction.objects.get(id=transaction_id)
            m_serializer = MessageSerializer(data=request.DATA, context={
                'request' : request,
                'transaction' : transaction,
                })

            if m_serializer.is_valid():
                m_serializer.save()
                return Response(m_serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(m_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Transaction.DoesNotExist:
            return Response({
                'detail' : 'Invalid transaction'
                }, status=status.HTTP_400_BAD_REQUEST)


class MessageListHandler(ListAPIView):

    serializer_class = MessageSerializer
    queryset = serializer_class.Meta.model.objects.all()
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by_param = '100'

    
