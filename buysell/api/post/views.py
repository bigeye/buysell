from django.http import Http404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from buysell.api.post.serializers import PostSerializer, TransactionSerializer
from buysell.api.post.models import Post, Transaction

class PostPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated()

class PostHandler(APIView):

    permission_classes = (PostPermission,)

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
            return Response(p_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(p_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

class PostListHandler(ListAPIView):

    serializer_class = PostSerializer
    queryset = serializer_class.Meta.model.objects.all()
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by_param = '100'

    permission_classes = (PostPermission,)

    def post(self, request, post_id=None, format=None):
        serializer = PostSerializer(data=request.DATA, context={
            'request' : request
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionHandler(APIView):

    def get(self, request, post_id=None, format=None):
        """Get Transaction when there is transaction created by user.
        """
        try:
            transaction = Transaction.objects.get(transaction=transaction_id,
                    requester=request.user)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            raise Http404
    
    def post(self, request, post_id=None, format=None):
        """Create Transaction if there is no transaction created by user.
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Http404

        t_serializer = TransactionSerializer(data=request.DATA, context = {
            'request' : request,
            'post' : post,
        })
        if t_serializer.is_valid():
            t_serializer.save()
            return Response(t_serializer.data, status=status.HTTP_200_OK)

        return Response(t_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(r_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(r_serializer.errors, status=sttus.HTTP_400_OK)

class MessageHandler(ListAPIView):

    def get(self, request, format=None):
        """Get a list of message of the transaction.
        """
        pass

    def post(self, request, format=None):
        """Create a new message on the transaction.
        """
        pass
