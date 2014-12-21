from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render_to_response, render
from django.template import RequestContext
from django.db.models import Q, Min, Max

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_decode_handler

from buysell.api.account.serializers import UserSerializer, UserSessionSerializer, \
                                            NotificationSerializer
from buysell.api.post.serializers import TransactionSerializer, MessageSerializer
from buysell.api.post.models import Transaction, Message
from buysell.api.account.models import UserProfile

from datetime import datetime
import operator


def main(request):
    return HttpResponse("<p>api.account.views.main</p><p>/account/</p>")


class SessionLoginHandler(APIView):
    """**SessionLoginHandler** class create sessions for users who try to login with
    common browsers.

    ## Note ##
    + Only **POST** method is allowed for login process.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/login.json"
                -d '{"username" : "elaborate", "password" : "1234"}'
                -H "Content-type: application/json"

    ## Response ##
        :::javascript
        /* On success - 200 */
        {
            "id" : 1,
            "username" : "elaborate",
            "email": "a@c.com",
            "last_name" : "Ahn",
            "first_name" : "Beunguk"
        }
        /* Invalid ID or password - 401 */
        {
            "non_field_errors": ["Unable to login with provided credentials."]
        }
        /* Bad request - 400 */
        {
            "username": ["This field is required."],
            "password": ["This field is required."]
        }
    """

    # Permission classe should be empty because nobody can be authenticated
    # before login.
    permission_classes = ()

    def post(self, request, format=None):
        serializer = UserSessionSerializer(data=request.DATA)

        if serializer.is_valid():
            user = serializer.object
            user_serializer = UserSerializer(user)
            login(request, user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_401_UNAUTHORIZED)


class SessionLogoutHandler(APIView):
    """**SessionLogoutHandler** class destroy sessions for users who request.

    ## Note ##
    + Only **GET** method is allowed for logout process.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/logout.json"

    ## Response ##
        :::javascript
        /* On success - 200 */
        {
            "id" : 1,
            "username" : "elaborate",
            "email": "a@c.com",
            "last_name" : "Ahn",
            "first_name" : "Beunguk"
        }
        /* User is not logged in - 403 */
        {
            "detail" : "Authentication credentials were not provided."
        }
    """

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        logout(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JWTLoginHandler(APIView):
    """**JWTLoginHandler** class auth token (Javascript Web Token) for user
    login.

    ## Note ##
    + Only **POST** method is allowed for logout process.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/auth_token.json"
                -d '{"username" : "elaborate", "password" : "1234"}'
                -H "Content-type: application/json"

    ## Response ##
        :::javascript
        /* On Success - 200 */
        {
            "token" : "{token_string}",
            "expire" : "2014-11-20T19:16:52"
        }
        /* Invalid ID or Password - 401 */
        {
            "non_field_errors": ["Unable to login with provided credentials."]
        }
    """

    # Permission classe should be empty because nobody can be authenticated
    # before login.
    permission_classes = ()

    def post(self, request, format=None):

        serializer = JSONWebTokenSerializer(data=request.DATA)

        if serializer.is_valid():
            token = serializer.object['token']
            pay_load = jwt_decode_handler(token)

            return Response({
                'token' : token,
                'expire' : datetime.fromtimestamp(pay_load['exp'])
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserHandler(APIView):
    """**RegistrationHandler** class handles user registration.

    ## Note ##
    + Only **POST** method is allowed for changing password.

    ## Request ##
        :::bash
        $ curl -X POST "http://exmaple.com/account/registration.json"
                -d '{"username" : "{username}", "password" : "{new_password}",
                    "email": "user@example.com", "last_name": "John",
                    "first_name": "Kim"}',
                -H "Content-type: application/json"

    ## Response ##
        :::javascript
        /* On success - 200 */
        {
            "id" : 1,
            "username" : "johnkim",
            "email": "user@example.com",
            "last_name" : "John",
            "first_name" : "Kim"
        }
        /* Bad request - 400 */
        {
            "email": ["Email field is required."],
            "password": ["This field is required."],
        }
        /* User is not logged in - 403 */
        {
            "detail" : "Authentication credentials were not provided."
        }
    """

    class UserHandlerPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            if request.method == 'POST':
                return True
            return request.user and request.user.is_authenticated()

    # Permission classe should be empty because nobody can be authenticated
    # before login.
    permission_classes = (UserHandlerPermission,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user, data=request.DATA, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        serializer = UserSerializer(request.user, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationHandler(APIView):

    def get(self, request):
        latest_msg = request.user.profile.latest_msg
        latest_id = 0
        if latest_msg is not None:
            latest_id = latest_msg.id

        msg_count = Message.objects.filter(Q(transaction__post__writer=self.request.user)\
                | Q(transaction__requester=self.request.user))\
                .filter(id__gt = latest_id).count()

        return Response({'count' : msg_count}, status=status.HTTP_200_OK)

    def put(self, request):

        msg = Message.objects.filter(Q(transaction__post__writer=self.request.user)\
                | Q(transaction__requester=self.request.user))\
                .order_by('-receive_date')

        if len(msg) > 0:
            profile = UserProfile.objects.get(user=request.user)
            profile.latest_msg = msg[0]
            profile.save()

        return Response({}, status=status.HTTP_200_OK)


class TransactionListHandler(ListAPIView):

    serializer_class = MessageSerializer
    model = Message
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by_param = '100'

    def get_queryset(self):

        msgs = Message.objects.filter(Q(transaction__post__writer=self.request.user)\
                | Q(transaction__requester=self.request.user))\
                .values('transaction_id').annotate(max_date=Max('receive_date'))
        filters = reduce(operator.or_, [(Q(transaction_id=m['transaction_id']) & \
            Q(receive_date=m['max_date'])) for m in msgs])
        queryset = Message.objects.filter(filters).order_by('-receive_date')

        return queryset
