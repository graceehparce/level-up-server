from configparser import NoSectionError
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

from levelupapi.models import game_type


class Game(models.Model):

    game_type = models.ForeignKey(
        "GameType", on_delete=models.CASCADE, related_name='game')
    title = models.CharField(max_length=250)
    maker = models.CharField(max_length=250)
    gamer = models.ForeignKey(
        "Gamer", on_delete=models.CASCADE, related_name='gamer')
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
