from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models.event_gamer import EventGamer
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer
from rest_framework.decorators import action


class EventView(ViewSet):

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.gamers.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.gamers.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.game = Game.objects.get(pk=request.data["game"])

        event.organizer = Gamer.objects.get(pk=request.data["organizer"])
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        events = []
        gamer = Gamer.objects.get(user=request.auth.user)

        if "game" in request.query_params:
            game_id = request.query_params['game']
            events = Event.objects.filter(
                game=game_id
            )

        else:
            events = Event.objects.all()

        for event in events:
            event.joined = gamer in event.gamers.all()

        serialized = EventSerializer(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        assigned_game = Game.objects.get(pk=request.data["game"])
        assigned_organizer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=assigned_organizer,
            game=assigned_game
        )

        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date',
                  'time', 'organizer', 'gamers', 'joined')
        depth = 1
