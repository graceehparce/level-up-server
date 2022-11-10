from configparser import NoSectionError
from django.db import models
from django.contrib.auth.models import User
from levelupapi.models.event_gamer import EventGamer
from levelupapi.models.gamer import Gamer


class Event(models.Model):

    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name='event_game')
    description = models.CharField(max_length=250)
    date = models.DateField(null=True, blank=True,
                            auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    organizer = models.ForeignKey(
        'Gamer', on_delete=models.CASCADE, related_name='event_organizer')
    gamers = models.ManyToManyField('Gamer', through='EventGamer')

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
