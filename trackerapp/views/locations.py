'''
A django page to handle all entries fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trackerapp.models import Location
from django.contrib.auth.models import User
from django.http import HttpResponse
import json


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        url = serializers.HyperlinkedIdentityField(
            view_name='location',
            lookup_field='id'
        )
        fields = ('id', 'name', 'route_id', 'route')
        depth = 1


class Locations(ViewSet):

    '''' a class to handle all the locations viewset

    Arguments:
        ViewSet '''

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        locations = Location.objects.all()

        serializer = LocationSerializer(
            locations, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''handles fetching ony one location'''
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(
                location, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")
