'''
A django page to handle all entries fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trackerapp.models import Entry, Event, Location, Route
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from datetime import datetime


class EntrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Entry
        url = serializers.HyperlinkedIdentityField(
            view_name='entry',
            lookup_field='id'
        )
        fields = ('id', 'date', 'time', 'attendee_count', 'vehicle_number',
                  'event_id', 'location_id', 'route_id', 'user_id', 'location', 'event')
        depth = 2


class Entries(ViewSet):

    '''' a class to handle all the entries viewset

    Arguments:
        ViewSet '''

    def create(self, request):
        ''' Handle POST operations and returns JSON serialized product instance'''

        newentry = Entry()
        newentry.date = datetime.now().strftime("%Y-%m-%d")
        newentry.time = datetime.now().strftime("%H:%M")
        newentry.attendee_count = request.data["attendee_count"]
        newentry.vehicle_number = request.data["vehicle_number"]
        newentry.event_id = request.data["event_id"]
        newentry.location_id = request.data["location_id"]
        newentry.route_id = request.data["route_id"]
        # newuser = User.objects.get(user=request.auth.user)
        # newentry.user = newuser
        newentry.user_id = request.data["user_id"]
        newentry.save()

        serializer = EntrySerializer(
            newentry, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        entries = Entry.objects.all()

        # handles fetching list of all entries from a certain location
        location_id = self.request.query_params.get('locationID', None)
        if location_id is not None:
            entries = entries.filter(location_id=location_id)

        # handles fetching list of all entries from a certain route
        route_id = self.request.query_params.get('routeID', None)
        if route_id is not None:
            entries = entries.filter(route_id=route_id)

        # handles fetching list of all entries from a certain event
        event_id = self.request.query_params.get('eventID', None)
        if event_id is not None:
            entries = entries.filter(event_id=event_id)

        serializer = EntrySerializer(
            entries, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''handles fetching only one entry'''
        try:
            entry = Entry.objects.get(pk=pk)
            serializer = EntrySerializer(
                entry, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")

    def update(self, request, pk=None):

        ogEntry = Entry.objects.get(pk=pk)
        ogEntry.attendee_count = request.data['attendee_count']
        ogEntry.vehicle_number = request.data['vehicle_number']

        ogEntry.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''handles delete product'''
        try:
            entry = Entry.objects.get(pk=pk)
            entry.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
