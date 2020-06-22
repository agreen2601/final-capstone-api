import json
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseServerError


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )

        fields = ('id', 'first_name', 'last_name', "last_login",
                  "username", "email", "date_joined",)


class Users(ViewSet):

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        users = User.objects.all()

        serializer = UserSerializer(
            users, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a user

        Returns:
            Response -- Empty body with 204 status code
        """
        user = User.objects.get(pk=pk)
        user.username = request.data["username"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def get_user(request):

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        token = req_body['token']
        user = Token.objects.get(key=token).user
        userdict = {
            "first": user.first_name,
            "last": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "token": token
        }
        return HttpResponse(json.dumps(userdict), content_type='application/json')
