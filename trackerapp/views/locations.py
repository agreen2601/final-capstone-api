'''
A django page to handle all places fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trackerapp.models import Place
from django.http import HttpResponse
import json


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        url = serializers.HyperlinkedIdentityField(
            view_name='place',
            lookup_field='id'
        )
        fields = ('id', 'name', 'route_id', 'route')
        depth = 1


class Places(ViewSet):

    '''' a class to handle all the places viewset

    Arguments:
        ViewSet '''

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        places = Place.objects.all()

        serializer = PlaceSerializer(
            places, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''handles fetching ony one place'''
        try:
            place = Place.objects.get(pk=pk)
            serializer = PlaceSerializer(
                place, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")
