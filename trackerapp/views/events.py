'''
A django page to handle all entries fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trackerapp.models import Event
from django.contrib.auth.models import User
from django.http import HttpResponse
import json


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'name')
        depth = 0


class Events(ViewSet):

    '''' a class to handle all the events viewset

    Arguments:
        ViewSet '''

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        events = Event.objects.all()

        serializer = EventSerializer(
            events, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''handles fetching ony one event'''
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(
                event, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")
