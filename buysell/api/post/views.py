from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from buysell.api.post.serializers import PostSerializer, PostRetreiveSerializer

class PostHandler(APIView):

    def get(self, request, post_id=None, format=None):

        data = { 'post_id' : post_id }
        serializer = PostRetreiveSerializer(data=data)

        if serializer.is_valid():
            p_serializer = PostSerializer(serializer.object)
            return Response(p_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(p_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id=None, format=None):

        data = { 'post_id' : post_id }
        serializer = PostRetreiveSerializer(data=data)

        if serializer.is_valid():
            p_serializer = PostSerializer(serializer.object, data=request.DATA, partial=True)
            if p_serializer.is_valid():
                p_serializer.save()
                return Response(p_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(p_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
