'''
A django page to handle all routes fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trackerapp.models import Route
from django.http import HttpResponse
import json


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Route
        url = serializers.HyperlinkedIdentityField(
            view_name='route',
            lookup_field='id'
        )
        fields = ('id', 'name', 'color', 'description')
        depth = 1


class Routes(ViewSet):

    '''' a class to handle all the routes viewset

    Arguments:
        ViewSet '''

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        routes = Route.objects.all()

        serializer = RouteSerializer(
            routes, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''handles fetching ony one Route'''
        try:
            route = Route.objects.get(pk=pk)
            serializer = RouteSerializer(
                Route, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")
